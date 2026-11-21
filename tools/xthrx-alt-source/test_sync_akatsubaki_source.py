import unittest
from sync_akatsubaki_source import BUNDLE_IDS, build_sources


def release(tag, version, prerelease, assets=None):
    return {
        "tag_name": tag,
        "name": f"{version} {'Nightly' if prerelease else 'Main'}",
        "body": f"Build {version}",
        "draft": False,
        "prerelease": prerelease,
        "published_at": "2026-11-21T12:00:00Z",
        "assets": assets if assets is not None else [{
            "name": "iSteam-ios.ipa",
            "browser_download_url": f"https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases/download/{tag}/iSteam-ios.ipa",
            "size": 123456,
        }],
    }


class AkatsubakiSourceSyncTests(unittest.TestCase):
    def test_maps_main_and_nightly_release_assets(self):
        source, pal = build_sources([
            release("main", "0.1.120", False),
            release("nightly", "0.1.121", True),
        ], {})
        self.assertEqual([app["bundleIdentifier"] for app in source["apps"]], [
            BUNDLE_IDS["main"], BUNDLE_IDS["nightly"],
        ])
        self.assertEqual(source["apps"][0]["versions"][0]["version"], "0.1.120")
        self.assertEqual(source["apps"][1]["versions"][0]["version"], "0.1.121")
        self.assertEqual(source["apps"][1]["versions"][0]["buildVersion"], "121")
        self.assertEqual(pal["apps"][1]["downloadURL"], source["apps"][1]["versions"][0]["downloadURL"])
        self.assertEqual(pal["apps"][1]["buildVersion"], "121")

    def test_ignores_tvos_assets(self):
        assets = [{
            "name": "iSteam-tvOS.ipa",
            "browser_download_url": "https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases/download/nightly/iSteam-tvOS.ipa",
            "size": 100,
        }]
        source, _ = build_sources([release("nightly", "0.1.121", True, assets)], {})
        self.assertEqual(source["apps"], [])

    def test_preserves_existing_app_when_release_is_missing(self):
        existing_app = {
            "name": "Akatsubaki Emu Nightly",
            "bundleIdentifier": BUNDLE_IDS["nightly"],
            "versions": [{
                "version": "0.1.009",
                "date": "2026-10-11T15:00:00Z",
                "downloadURL": "https://akatsubaki-emu.github.io/downloads/iSteam-nightly.ipa",
            }],
        }
        source, pal = build_sources([], {"apps": [existing_app]})
        self.assertEqual(len(source["apps"]), 1)
        self.assertEqual(source["apps"][0]["versions"][0]["version"], "0.1.009")
        self.assertEqual(pal["apps"][0]["downloadURL"], existing_app["versions"][0]["downloadURL"])

    def test_normalizes_case_variant_legacy_bundle_id(self):
        existing_app = {
            "name": "Akatsubaki Emu Nightly",
            "bundleIdentifier": "com.Xthrx.iSteam.Nightly",
            "versions": [{
                "version": "0.2.1",
                "buildVersion": "3",
                "date": "2026-10-10T13:06:07Z",
                "downloadURL": "https://akatsubaki-emu.github.io/downloads/iSteam-nightly.ipa",
            }],
        }
        source, _ = build_sources([], {"apps": [existing_app]})
        self.assertEqual(source["apps"][0]["bundleIdentifier"], BUNDLE_IDS["nightly"])
        self.assertEqual(source["apps"][0]["versions"][0]["version"], "0.2.1")

    def test_rejects_release_without_semver(self):
        item = release("main", "unversioned", False)
        source, _ = build_sources([item], {})
        self.assertEqual(source["apps"], [])

    def test_rejects_download_outside_canonical_repository(self):
        item = release("nightly", "0.1.121", True)
        item["assets"][0]["browser_download_url"] = "https://example.com/iSteam-ios.ipa"
        source, _ = build_sources([item], {})
        self.assertEqual(source["apps"], [])


if __name__ == "__main__":
    unittest.main()
