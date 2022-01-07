from portfolio_generator.validate import validate


class TestValidate:
    def test_template_01(self):
        o = {"template": "filename"}
        assert validate(o) is None

    def test_template_02(self):
        o = {}
        assert validate(o) == "invalid: {'template': ['required field']}"

    def test_template_03(self):
        o = "a:b:c"
        assert validate(o) == "invalid: must be of dict type"

    def test_names_01(self):
        o = {"template": "filename", "names": {"github": "atu4403"}}
        assert validate(o) is None

    def test_names_02(self):
        o = {"template": "filename", "names": {"github2": "atu4403"}}
        assert validate(o) == "invalid: {'names': [{'github2': ['unknown field']}]}"

    def test_names_03(self):
        o = {"template": "filename", "names": {"zenn": 1}}
        assert validate(o) == "invalid: {'names': [{'zenn': ['must be of string type']}]}"

    def test_apis_01(self):
        # https://stackoverflow.com/questions/70087015/in-cerberus-python-is-there-a-way-to-create-a-schema-that-allows-any-key-name
        o = {"template": "filename", "apis": {"other_api": {"type": "json", "url": "url1"}}}
        assert validate(o) is None

    def test_apis_02(self):
        o = {"template": "filename", "apis": "test"}
        assert validate(o) == "invalid: {'apis': ['must be of dict type']}"

    def test_apis_03(self):
        o = {"template": "filename", "apis": ["test"]}
        assert validate(o) == "invalid: {'apis': ['must be of dict type']}"

    def test_apis_04(self):
        o = {"template": "filename", "apis": {"other_api": {"type": "json"}}}
        assert validate(o) == "invalid: {'apis': [{'other_api': [{'url': ['required field']}]}]}"
