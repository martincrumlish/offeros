(function () {
  var reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function markRevealTargets() {
    var targets = document.querySelectorAll(".opk-section, .opk-card, .opk-price-strip, .opk-vsl-frame");
    targets.forEach(function (target) {
      target.setAttribute("data-opk-reveal", "");
    });
  }

  function initReveal() {
    if (reducedMotion || !("IntersectionObserver" in window)) {
      document.querySelectorAll("[data-opk-reveal]").forEach(function (target) {
        target.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

    document.querySelectorAll("[data-opk-reveal]").forEach(function (target) {
      observer.observe(target);
    });
  }

  function initVideoButtons() {
    document.querySelectorAll("[data-opk-video-play], [data-offeros-video-play]").forEach(function (button) {
      button.addEventListener("click", function () {
        var frame = button.closest("[data-offeros-hero-video], .opk-vsl-frame");
        var video = frame && frame.querySelector("video");

        if (video && typeof video.play === "function") {
          video.setAttribute("controls", "controls");
          video.play();
          button.hidden = true;
          return;
        }

        frame && frame.setAttribute("data-opk-video-requested", "true");
        button.setAttribute("aria-pressed", "true");
      });
    });
  }

  function normalizeCtas() {
    document.querySelectorAll("[data-offeros-cta]").forEach(function (cta) {
      if (!cta.getAttribute("href")) {
        cta.setAttribute("href", "#checkout");
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    normalizeCtas();
    markRevealTargets();
    initReveal();
    initVideoButtons();
  });
})();
