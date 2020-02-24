import zeep

class ZeepPatch:
    # Work arround: NotImplementedError: AnySimpleType.pytonvalue() not implemented
    def _patched_zeep_pythonvalue(self, xmlvalue):
        return xmlvalue

    def Patch(self):
        # Patch zeep.xsd.AnySimpleType.pythonvalue 
        zeep.xsd.AnySimpleType.pythonvalue = self._patched_zeep_pythonvalue