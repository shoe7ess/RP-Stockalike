// RP-Stock calendar: shows the game date starting at the first era (Year 1 -> 1945 by default).
// Display only: the game's real clock (UT), orbits and contract timers are untouched.
// Kerbin time: "Year 1945, Day 12". With "Show as Earth time" on: a real calendar date, "12 Jan 1945".
// Configure with:  RPSTOCK_CALENDAR { startYear = 1945 }
using System;
using System.Text.RegularExpressions;
using UnityEngine;

namespace RPStock
{
    public class OffsetDateFormatter : IDateTimeFormatter
    {
        readonly IDateTimeFormatter inner;
        readonly int offset;   // added to the stock year number (stock Year 1 = startYear)
        readonly DateTime epoch;   // Earth-time mode: UT 0 = 1 January of startYear

        public OffsetDateFormatter(IDateTimeFormatter inner, int startYear)
        {
            this.inner = inner;
            offset = startYear - 1;
            epoch = new DateTime(Math.Max(1, startYear), 1, 1, 0, 0, 0, DateTimeKind.Utc);
        }

        // With "Show as Earth time" on, print real calendar dates (e.g. "4 Oct 1957") so the game date can be
        // read directly against the historical dates in contract descriptions.
        bool EarthCalendar(double time) => !GameSettings.KERBIN_TIME && time >= 0 && time < 3e11;
        string Earth(double time, bool includeTime, bool includeSeconds, bool compact)
        {
            DateTime dt = epoch.AddSeconds(Math.Floor(time));
            string date = compact ? dt.ToString("yyyy-MM-dd") : dt.ToString("d MMM yyyy", System.Globalization.CultureInfo.InvariantCulture);
            if (!includeTime) return date;
            return date + (compact ? " " : ", ") + dt.ToString(includeSeconds ? "HH:mm:ss" : "HH:mm");
        }

        string Shift(double time, string s)
        {
            if (string.IsNullOrEmpty(s) || offset == 0 || double.IsNaN(time) || double.IsInfinity(time) || time < 0) return s;
            int yearLen = inner.Year;
            if (yearLen <= 0) return s;
            long year = (long)Math.Floor(time / yearLen) + 1;
            // the year is the first number in stock's date strings ("Year 3, Day 12", "Y3, D12")
            var rx = new Regex(@"(?<!\d)" + year + @"(?!\d)");
            return rx.Replace(s, (year + offset).ToString(), 1);
        }

        // absolute dates get the era offset
        public string PrintDate(double time, bool includeTime, bool includeSeconds = false) =>
            EarthCalendar(time) ? Earth(time, includeTime, includeSeconds, false) : Shift(time, inner.PrintDate(time, includeTime, includeSeconds));
        public string PrintDateNew(double time, bool includeTime) =>
            EarthCalendar(time) ? Earth(time, includeTime, false, false) : Shift(time, inner.PrintDateNew(time, includeTime));
        public string PrintDateCompact(double time, bool includeTime, bool includeSeconds = false) =>
            EarthCalendar(time) ? Earth(time, includeTime, includeSeconds, true) : Shift(time, inner.PrintDateCompact(time, includeTime, includeSeconds));

        // durations and timestamps stay exactly as stock
        public string PrintTimeLong(double time) => inner.PrintTimeLong(time);
        public string PrintTimeStamp(double time, bool days = false, bool years = false) => inner.PrintTimeStamp(time, days, years);
        public string PrintTimeStampCompact(double time, bool days = false, bool years = false) => inner.PrintTimeStampCompact(time, days, years);
        public string PrintTime(double time, int valuesOfInterest, bool explicitPositive) => inner.PrintTime(time, valuesOfInterest, explicitPositive);
        public string PrintTime(double time, int valuesOfInterest, bool explicitPositive, bool logEnglish) => inner.PrintTime(time, valuesOfInterest, explicitPositive, logEnglish);
        public string PrintTimeCompact(double time, bool explicitPositive) => inner.PrintTimeCompact(time, explicitPositive);
        public string PrintDateDelta(double time, bool includeTime, bool includeSeconds, bool useAbs) => inner.PrintDateDelta(time, includeTime, includeSeconds, useAbs);
        public string PrintDateDeltaCompact(double time, bool includeTime, bool includeSeconds, bool useAbs) => inner.PrintDateDeltaCompact(time, includeTime, includeSeconds, useAbs);
        public string PrintDateDeltaCompact(double time, bool includeTime, bool includeSeconds, bool useAbs, int interestedPlaces) => inner.PrintDateDeltaCompact(time, includeTime, includeSeconds, useAbs, interestedPlaces);
        public int Minute => inner.Minute;
        public int Hour => inner.Hour;
        public int Day => inner.Day;
        public int Year => inner.Year;
    }

    [KSPAddon(KSPAddon.Startup.MainMenu, true)]
    public class RPStockCalendar : MonoBehaviour
    {
        public void Start()
        {
            int startYear = 1945; bool found = false;
            foreach (ConfigNode n in GameDatabase.Instance.GetConfigNodes("RPSTOCK_CALENDAR"))
            {
                found = true;
                if (n.HasValue("startYear")) int.TryParse(n.GetValue("startYear"), out startYear);
            }
            if (!found) return;   // config is skipped when RP-0/RP-1 is installed
            IDateTimeFormatter current = KSPUtil.dateTimeFormatter;
            if (current is OffsetDateFormatter) return;
            if (current == null || current.GetType() != typeof(KSPUtil.DefaultDateTimeFormatter))
            {
                // another calendar mod (e.g. Kronometer) owns the clock - leave it alone
                Debug.Log("[RP-Stock] Custom calendar already installed (" + current?.GetType().Name + "); not changing the date display.");
                return;
            }
            KSPUtil.dateTimeFormatter = new OffsetDateFormatter(current, startYear);
            Debug.Log("[RP-Stock] Calendar: Year 1 is shown as " + startYear + ".");
        }
    }
}
