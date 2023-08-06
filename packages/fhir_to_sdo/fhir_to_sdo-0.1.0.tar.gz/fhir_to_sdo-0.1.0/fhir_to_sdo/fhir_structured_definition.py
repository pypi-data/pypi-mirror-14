# Copyright (c) 2016, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the Mayo Clinic nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
from jsonasobj import JsonObj, load, loads
from typing import Union, List
from requests import get

fname = str
json_txt = str
# TODO: find typing definition for something that supports read() (stream?)

# A map from the FHIR primitive types (definitions that contain "_code" in one of the types) to
# the equivalent schema.org datatype
type_map = {'base64binary': 'Text',
            'boolean': 'Boolean',
            'code': 'Text',
            'date': 'Date',
            'dateTime': 'DateTime',
            'decimal': 'Number',
            'id': 'Text',
            'instant': 'DateTime',
            'integer': 'Number',
            'markdown': 'Text',
            'oid': 'Text',
            'positiveint': 'Number',
            'string': 'Text',
            'time': 'Time',
            'unsignedint': 'Number',
            'uri': 'Text',
            'uuid': 'Text'}


def dotted_root(path: str) -> str:
    """ Return the root of a dotted path
    :param path: dotted path
    :return: dotted path sans rightmost node
    """
    return path.rsplit('.', 1)[0]


def dotted_leaf(path: str) -> str:
    """ Return the 'leaf' of a dotted path
    :param path: dotted path
    :return: rightmost node of dotted path
    """
    return path.split('.')[-1]


def url_root(path: str) -> str:
    """ return the root of a slash or hash-separated URL
    :param path: url
    :return: """
    return path.rsplit('#', 1)[0] if '#' in path else path.rsplit('#', 1)[0]


def tip(path: str) -> str:
    """ return the 'leaf' of a slash or hash-separated URL
    :param path: url
    :return:
    """
    return path.split('#')[-1] if '#' in path else path.split('/')[-1]


def esc(text: str) -> str:
    """ Simple XML text escape """
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def fix_url(url: str) -> str:
    """ A function to replace the official FHIR URL with an equivalent """
    if '/StructureDefinition/' in url:
        return url.replace('http://hl7.org/fhir/StructureDefinition/', 'http://schema.org/')
    else:
        return url.replace('http://hl7.org/fhir/ValueSet/', 'http://schema.org/')


class FHIRStructuredDefinition:
    def __init__(self, source: Union[fname, json_txt]) -> None:
        """ Construct a FHIR StructuredDefinition from a source file name, file or string
        :param source: JSON source
        """
        if hasattr(source, 'read'):
            self._obj = load(source)
        elif source.strip().startswith('{'):
            self._obj = loads(source)
        else:
            self._obj = load(open(source))
        self.elements = [FHIRElement(self._obj, e) for e in self._obj.snapshot.element
                         if '.' in e.path and self._significant_differential(e)]

    def should_process(self) -> bool:
        """ Return True if this structured definition should be included as part of schema.org entry
        :return:
        """
        # The presence of a "_code" in a type variable instead of "code" seems to be indicitive of a primitive type
        return not any(['_code' in typ for typ in [el.type for el in self._obj.snapshot.element if 'type' in el]])

    def _significant_differential(self, sse: JsonObj) -> bool:
        """ Determine whether the Snapshot Element in sse is considered significant from a schema.org perspective """
        for e in self._obj.differential.element:
            if e.path == sse.path and 'type' in e:
                for t in e.type:
                    if 'code' in t:
                        return True
        return False

    def sdo_class(self):
        url = fix_url(self._obj.url)
        name = esc(self._obj.name)
        description = esc(self._obj.description)
        baseDefinition = fix_url(self._obj.baseDefinition) if 'baseDefinition' in self._obj else "http://schema.org/CreativeWork"
        baseType = 'fhir:' + self._obj.baseType if 'baseType' in self._obj else 'CreativeWork'
        return """<div typeof="rdfs:Class" resource="%(url)s">
  <span class="h" property="rdfs:label">fhir:%(name)s</span>
  <span property="rdfs:comment">%(description)s</span>
  <span>Subclass of: <a property="rdfs:subClassOf" href="%(baseDefinition)s">%(baseType)s</a></span>
  <link property="http://schema.org/isPartOf" href="http://fhir.schema.org" />
</div>""" % vars()

    def sdo_properties(self):
        return '\n\t'.join([e.sdo_property() for e in self.elements])


class FHIRElement:
    def __init__(self, owner: FHIRStructuredDefinition, ele: JsonObj) -> None:
        """ An Element in a FHIR Structured Definition.
        :param owner:  Owning FHIR Structured Definition
        :param ele: JSON of snapshot element
        """
        self._obj = ele
        self._obj.fullUrl = fix_url(url_root(owner.url) + '/' + ele.path)
        self._obj.ownerUrl = fix_url(owner.url)
        self._obj.ownerLabel = esc(owner.name)
        if 'definition' not in ele:
            self._obj.definition = "No definition supplied"
        else:
            self._obj.definition = esc(self._obj.definition)

    def sdo_property(self):
        if self._obj.path.endswith('[x]'):
            path = self._obj.path.replace('[x]', '')
            baseurl = self._obj.fullUrl.replace('[x]', '')
            return '\n\t'.join([self._sdo_property_choice(path, baseurl, t) for t in self._obj.type])
        else:
            return self._sdo_property_instance([t for t in self._obj.type])

    def _sdo_property_choice(self, path: str, baseurl: str, typ: JsonObj) -> str:
        self._obj.path = path + typ.code
        self._obj.fullUrl = fix_url(baseurl + typ.code)
        return self._sdo_property_instance([typ])

    def _sdo_property_instance(self, types: List[JsonObj]) -> str:
        """ Return a schema.org property entry for the supplied type entry
        :param types: Element "type" entry -- references a list of codes
        :return: schema.org Property entry
        """
        self._obj.typeList = FHIRTypes(self, types).sdo_range()
        return """<div typeof="rdf:Property" resource="%(fullUrl)s">
      <span class="h" property="rdfs:label">fhir:%(path)s</span>
      <span property="rdfs:comment">%(definition)s</span>
      <span>Domain: <a property="http://schema.org/domainIncludes" href="%(ownerUrl)s">fhir:%(ownerLabel)s</a></span>
      %(typeList)s
      <link property="http://schema.org/isPartOf" href="http://fhir.schema.org" />
    </div>""" % self._obj._as_dict


class FHIRTypes:
    def __init__(self, owner: FHIRElement, types: List[JsonObj]):
        """ A FHIR Type entry.  typ is guaranteed to have at least one element with a 'code' entry """
        self._types = [FHIRType(owner._obj, t) for t in types]

    def sdo_range(self):
        return '\n\t'.join([t.sdo_range() for t in self._types])


class FHIRType:
    def __init__(self, owner: JsonObj, typ: JsonObj) -> None:
        """ Process a  type entry in a set of types for a FHIR Element
        :param owner: Containing FHIR Element
        :param typ: entry in element "type" list
        """
        self._type = typ
        if typ.code in ('code', 'CodeableConcept') and 'binding' in owner:
            if 'valueSetReference' in owner.binding:
                ref = owner.binding.valueSetReference.reference
                if owner.binding.strength == "required":
                    defined_value_sets.add(ref)
            elif 'valueSetUri' in owner.binding:
                ref = owner.binding.valueSetUri
            else:
                ref = "http://schema.org/Text"
            self._type.typeUrl = ref
            self._type.typeCode = tip(ref)
        else:
            if typ.code == 'Reference' and 'profile' in typ:
                assert len(typ.profile) == 1
                code = tip(typ.profile[0])
            else:
                code = type_map.get(typ.code, typ.code)
            self._type.typeUrl = url_root(owner.ownerUrl) + '/' + code
            self._type.typeCode = code

    def sdo_range(self):
        typeUrl = fix_url(self._type.typeUrl)
        typeCode = esc(self._type.typeCode)
        return '<span>Range: <a property="http://schema.org/rangeIncludes" href="%(typeUrl)s">%(typeCode)s</a></span>' \
               % vars()


class FHIRValueSetRefs:
    def __init__(self):
        self.defined_sets = dict()

    def add(self, ref: str) -> None:
        if ref not in self.defined_sets:
            self.defined_sets[ref] = FHIRValueSetReference(ref)

    def sdo_valuesets(self):
        return '\n\t'.join([e.sdo_valueset() for e in self.defined_sets.values()])

# Defined value sets
defined_value_sets = FHIRValueSetRefs()


class FHIRValueSetReference:
    def __init__(self, reference: str) -> None:
        """ A value set reference container
        :param reference: URI of the reference value set
        """
        self._reference = reference

    def sdo_valueset(self):
        """ Return a schema.org representation of the value set
        :return:
        """
        # TODO: This URL should really be a terminology service expand call, but the documented method doesn't work
        resp = get(self._reference, headers={'accept': 'application/json'})
        rval = ''
        if resp.ok:
            vsdef = loads(resp.text)
            rval = self.sdo_valueset_header(vsdef.url, vsdef.id, vsdef.name)
            if 'codeSystem' in vsdef and 'concept' in vsdef.codeSystem:
                cs = vsdef.codeSystem
                rval += '\n\t'.join([self.sdo_concept(vsdef.url, vsdef.id, cs.system, c) for c in cs.concept])
        else:
            print("ValueSet access error: %s (%s)" % (self._reference, resp.reason))
        return rval

    @staticmethod
    def sdo_valueset_header(uri: str, name: str, description: str,
                            parenturi: str="http://schema.org/Enumeration", parentname: str="Enumeration") -> str:
        name = esc(name)
        description = esc(description)
        parentname = esc(parentname)
        fullUri = fix_url(uri)
        return """<div typeof="rdfs:Class" resource="%(fullUri)s">
  <span class="h" property="rdfs:label">fhir:%(name)s</span>
  <span property="rdfs:comment">%(description)s</span>
  <span>Subclass of: <a property="rdfs:subClassOf" href="%(parenturi)s">fhir:%(parentname)s</a></span>
  <link property="http://schema.org/isPartOf" href="http://fhir.schema.org" />
</div>""" % vars()

    def sdo_concept(self, parenturi: str, parentname: str, codesystem: str, concept: JsonObj) -> str:
        # TODO: this needs to be fixed
        #  Double escape on the code to allow reserialize then parse
        uri = codesystem + '/' + esc(esc(concept.code))
        sdouri = 'http://fhir.schema.org/' + esc(esc(concept.code))
        parenturi = fix_url(parenturi)
        name = esc(concept.code)
        description = esc(concept.definition) if 'definition' in concept else "UNDEFINED"
        return """<div typeof="%(parenturi)s" resource="%(sdouri)s">
  <span class="h" property="rdfs:label">fhir:%(name)s</span>
  <span property="rdfs:comment">%(description)s</span>
  <span>type: <a href="%(parenturi)s">fhir:%(parentname)s</a></span>
  <link property="owl:equivalentClass" href="%(uri)s"/>
  <link property="http://schema.org/isPartOf" href="http://fhir.schema.org" />
</div>""" % vars()
