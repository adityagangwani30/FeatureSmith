from importlib import import_module


def test_workspace_packages_import() -> None:
    import_module("featuresmith")
    import_module("featuresmith.api")
    import_module("featuresmith_cli")
    import_module("featuresmith_dashboard")
