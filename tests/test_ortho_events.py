"""Dated orthodontic events retain logistics outside the reusable slide decks."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
M1 = ROOT / "events/2026-11-30-orthodontic-informatics-module1"
M3 = ROOT / "events/2026-11-20-orthodontic-informatics-module3"
TITLE1 = "Data Sharing, Integration, and Transition in Orthodontic Informatics"
TITLE3 = "AI and Reusable Clinical Data"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.elements = []
        self.text = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)

    @property
    def visible(self):
        return " ".join(" ".join(self.text).split())


class OrthoEvents(unittest.TestCase):
    def test_module1_announcement_has_supplied_logistics(self):
        self.assertTrue((M1 / "index.html").is_file(), "Module 1 announcement missing")
        page = Page(M1 / "index.html")
        for text in [TITLE1, "Orthodontic Informatics · Module 1", "first-year orthodontic residents",
                     "Monday, November 30, 2026", "3:00", "4:00 p.m.", "Eastern",
                     "EST (UTC−05:00)", "Ortho seminar room",
                     "School of Dental Medicine – Orthodontics", "Case Western Reserve University"]:
            self.assertIn(text, page.visible)
        times = [attrs["datetime"] for tag, attrs in page.elements if tag == "time"]
        self.assertEqual(times, ["2026-11-30", "2026-11-30T15:00:00-05:00", "2026-11-30T16:00:00-05:00"])
        self.assertIn(("a", {"class": "event-secondary", "href": "../../slides/orthodontic-informatics/module1/"}), page.elements)

    def test_module3_records_supplied_presentation_time(self):
        self.assertTrue((M3 / "index.html").is_file(), "Module 3 presentation record missing")
        page = Page(M3 / "index.html")
        for text in [TITLE3, "Orthodontic Informatics · Module 3", "second-year orthodontic residents",
                     "Presented", "Friday, November 20, 2026", "10:00", "11:00 a.m.", "Eastern",
                     "Back seminar room", "School of Dental Medicine – Orthodontics"]:
            self.assertIn(text, page.visible)
        self.assertEqual([attrs["datetime"] for tag, attrs in page.elements if tag == "time"],
                         ["2026-11-20", "2026-11-20T10:00:00-05:00", "2026-11-20T11:00:00-05:00"])
        self.assertIn("View current slides", page.visible)
        self.assertTrue(any(a.get("href") == "../../slides/orthodontic-informatics/module3/" for t, a in page.elements if t == "a"))
        for text in ["Time not recorded", "all-day", "Add to calendar", ".ics"]:
            self.assertNotIn(text, (M3 / "index.html").read_text())
        self.assertEqual(list(M3.glob("*.ics")), [])

    def test_module1_calendar_matches_page_without_losing_fold_spaces(self):
        from datetime import datetime
        from zoneinfo import ZoneInfo
        self.assertTrue((M1 / "orthodontic-informatics-module1.ics").is_file(), "Module 1 calendar missing")
        raw = (M1 / "orthodontic-informatics-module1.ics").read_bytes()
        self.assertTrue(raw.endswith(b"\r\n"))
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
        self.assertTrue(all(len(line) <= 75 for line in raw.split(b"\r\n")))
        unfolded = raw.replace(b"\r\n ", b"").decode()
        fields = dict(line.split(":", 1) for line in unfolded.split("\r\n") if ":" in line)
        def unescape(value):
            return value.replace("\\n", "\n").replace("\\,", ",").replace("\\;", ";").replace("\\\\", "\\")
        self.assertEqual(unescape(fields["SUMMARY"]), TITLE1)
        self.assertEqual(unescape(fields["LOCATION"]), "Ortho seminar room, School of Dental Medicine – Orthodontics, Case Western Reserve University")
        self.assertEqual(fields["DTSTART"], "20261130T200000Z")
        self.assertEqual(fields["DTEND"], "20261130T210000Z")
        self.assertEqual(fields["URL"], "https://open-ortho.org/lectures/events/2026-11-30-orthodontic-informatics-module1/")
        self.assertEqual(fields["UID"], "2026-11-30-orthodontic-informatics-module1@open-ortho.org")
        stamp = datetime.strptime(fields["DTSTAMP"], "%Y%m%dT%H%M%SZ")
        self.assertEqual(stamp.year, 2026)
        start = datetime.strptime(fields["DTSTART"], "%Y%m%dT%H%M%SZ").replace(tzinfo=ZoneInfo("UTC"))
        self.assertEqual(start.astimezone(ZoneInfo("America/New_York")).isoformat(), "2026-11-30T15:00:00-05:00")
        page = Page(M1 / "index.html")
        description = next(a["content"] for t, a in page.elements if t == "meta" and a.get("name") == "description")
        self.assertEqual(unescape(fields["DESCRIPTION"]), description)
        self.assertIn(description, page.visible)
        self.assertTrue(any(t == "a" and a.get("href") == "orthodontic-informatics-module1.ics" and "download" in a for t, a in page.elements))
        for iso, weekday in [("2026-11-30", "Monday"), ("2026-11-20", "Friday")]:
            self.assertEqual(datetime.fromisoformat(iso).strftime("%A"), weekday)

    def test_presentation_history_and_event_maintenance_have_separate_owners(self):
        import re
        catalog = (ROOT / "slides/orthodontic-informatics/index.html").read_text()
        for directory, module in [(M1, "module1"), (M3, "module3")]:
            self.assertTrue((directory / "README.md").is_file(), "Event maintenance guide missing")
            guide = (directory / "README.md").read_text()
            self.assertIn("../README.md", guide)
            self.assertIn("evolving", guide)
            self.assertIn("user-provided", guide)
            self.assertIn("not an immutable", guide)
            page = Page(directory / "index.html")
            abstract = next(a["content"] for t, a in page.elements if t == "meta" and a.get("name") == "description")
            self.assertIn(abstract, guide)
            deck_guide = (ROOT / "slides/orthodontic-informatics" / module / "README.md").read_text()
            self.assertIn("## Presentation history", deck_guide)
            self.assertIn("../../../events/" + directory.name + "/", deck_guide)
            self.assertIn("../../events/" + directory.name + "/", catalog)
            for label, link in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", guide):
                if "://" not in link and link != "../README.md":
                    self.assertTrue((directory / link.split("#")[0]).exists(), link)

    def test_shared_layout_local_assets_and_speaker_contract(self):
        for directory in [M1, M3]:
            page = Page(directory / "index.html")
            styles = [a["href"] for t, a in page.elements if t == "link" and a.get("rel") == "stylesheet"]
            self.assertEqual(styles, ["../../assets/css/index.css", "../event.css"])
            self.assertFalse(any(t in {"style", "script"} or "style" in a for t, a in page.elements))
            self.assertEqual(list(directory.glob("*.css")), [])
            self.assertEqual([(a.get("src"), a.get("alt")) for t, a in page.elements if t == "img"], [("../../assets/img/amagni.jpeg", "Toni Magni")])
            for text in ["Toni Magni", "Clinical Instructor", "Department of Orthodontics", "School of Dental Medicine", "Case Western Reserve University"]:
                self.assertIn(text, page.visible)
            for tag, attrs in page.elements:
                for key in ["href", "src"]:
                    link = attrs.get(key, "")
                    if link and not link.startswith(("https:", "mailto:", "#")):
                        self.assertTrue((directory / link).exists(), link)
            self.assertTrue(any(t == "a" and a.get("href") == "../../" for t, a in page.elements))
            for street in ["Carnegie", "Cornell", "2124"]:
                self.assertNotIn(street, (directory / "index.html").read_text())


if __name__ == "__main__":
    unittest.main()
