var _paq = window._paq = window._paq || [];
_paq.push(['requireConsent']);
_paq.push(['trackPageView']);
_paq.push(['enableLinkTracking']);
(function() {
  var u = "https://piwik.cebitec.uni-bielefeld.de/";
  _paq.push(['setTrackerUrl', u + 'matomo.php']);
  _paq.push(['setSiteId', '22']);
  var d = document, g = d.createElement('script'), s = d.getElementsByTagName('script')[0];
  g.async = true; g.src = u + 'matomo.js'; s.parentNode.insertBefore(g, s);
})();

// Material writes consent to localStorage under key "__consent"
function applyMatomoConsent() {
  try {
    var c = JSON.parse(localStorage.getItem('__consent') || '{}');
    if (c.analytics === 'accepted') {
      _paq.push(['setConsentGiven']);
      _paq.push(['setCookieConsentGiven']);
    } else {
      _paq.push(['forgetConsentGiven']);
    }
  } catch (e) {}
}
applyMatomoConsent();
window.addEventListener('storage', applyMatomoConsent); // reflect changes made in other tabs