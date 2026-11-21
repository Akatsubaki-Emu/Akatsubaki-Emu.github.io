import unittest
from build_xthrx_repo import build, merge_apps, normalize_app, unpack

class SourceBuilderTests(unittest.TestCase):
    def test_unpack_common_layouts(self):
        self.assertEqual(unpack({"source": {"apps": [{"name": "A"}]}}), [{"name": "A"}])
        self.assertEqual(unpack({"apps": {"one": {"name": "A"}}}), [{"name": "A"}])
        self.assertEqual(unpack([{"name": "A"}]), [{"name": "A"}])

    def test_legacy_record_is_normalized_for_sidestore(self):
        app = normalize_app({
            "name": "Example", "bundleID": "com.example.app", "developer": "Example Dev",
            "version": "1.2", "versionDate": "2026-11-20",
            "downloadURL": "https://example.test/app.ipa", "versionDescription": "First release",
        })
        self.assertIsNotNone(app)
        self.assertEqual(app["bundleIdentifier"], "com.example.app")
        self.assertEqual(app["developerName"], "Example Dev")
        self.assertEqual(app["versions"][0]["version"], "1.2")
        self.assertEqual(app["versions"][0]["size"], 0)
        self.assertEqual(app["versions"][0]["localizedDescription"], "First release")

    def test_rejects_missing_identity_and_download(self):
        self.assertIsNone(normalize_app({"name": "No bundle", "version": "1"}))
        self.assertIsNone(normalize_app({
            "name": "No URL", "bundleIdentifier": "com.example.no-url", "version": "1",
        }))
        self.assertIsNone(normalize_app({
            "name": "Bad URL", "bundleIdentifier": "com.example.bad",
            "version": "1", "downloadURL": "javascript:alert(1)",
        }))

    def test_deduplicates_bundle_ids_but_keeps_distinct_versions(self):
        first = normalize_app({
            "name": "Example", "bundleIdentifier": "com.example.app", "version": "1.0",
            "date": "2026-01-01", "downloadURL": "https://one.test/app.ipa",
        })
        second = normalize_app({
            "name": "Example Updated", "bundleIdentifier": "com.example.app", "version": "2.0",
            "date": "2026-11-20", "downloadURL": "https://two.test/app.ipa",
        })
        result = merge_apps([
            {"name": "First", "url": "https://one.test/source.json", "status": "ok", "apps": [first]},
            {"name": "Second", "url": "https://two.test/source.json", "status": "ok", "apps": [second]},
        ])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Example Updated")
        self.assertEqual(result[0]["versions"][0]["version"], "2.0")
        self.assertEqual(len(result[0]["versions"]), 2)
        self.assertEqual(result[0]["xthrxSources"], ["First", "Second"])

    def test_build_deduplicates_feed_urls_and_reports_failures(self):
        manifest = {"sources": [
            {"name": "One", "url": "https://one.test/source.json"},
            {"name": "Duplicate", "url": "https://one.test/source.json"},
            {"name": "Two", "url": "https://two.test/source.json"},
        ]}
        app = normalize_app({
            "name": "Example", "bundleIdentifier": "com.example.app",
            "version": "1", "downloadURL": "https://one.test/app.ipa",
        })
        fixtures = {
            "https://one.test/source.json": {
                "name": "One", "url": "https://one.test/source.json", "status": "ok",
                "apps": [app], "appCount": 1, "validApps": 1, "rejectedApps": 0,
            },
            "https://two.test/source.json": {
                "name": "Two", "url": "https://two.test/source.json",
                "status": "failed", "error": "fixture failure",
            },
        }
        catalogue, report = build(manifest, fetcher=lambda source: fixtures[source["url"]])
        self.assertEqual(report["configuredFeeds"], 2)
        self.assertEqual(report["acceptedFeeds"], 1)
        self.assertEqual(report["failedFeeds"], 1)
        self.assertEqual(len(catalogue["apps"]), 1)

if __name__ == "__main__":
    unittest.main()
