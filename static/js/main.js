(() => {
  "use strict";

  const menuButton = document.querySelector(".menu-toggle");
  const navigation = document.querySelector(".primary-nav");

  if (menuButton && navigation) {
    menuButton.addEventListener("click", () => {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
      menuButton.setAttribute("aria-label", isOpen ? "Open navigation" : "Close navigation");
      navigation.classList.toggle("is-open", !isOpen);
    });

    navigation.addEventListener("click", (event) => {
      if (event.target.closest("a")) {
        menuButton.setAttribute("aria-expanded", "false");
        menuButton.setAttribute("aria-label", "Open navigation");
        navigation.classList.remove("is-open");
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
        menuButton.setAttribute("aria-expanded", "false");
        menuButton.setAttribute("aria-label", "Open navigation");
        navigation.classList.remove("is-open");
        menuButton.focus();
      }
    });
  }

  document.querySelectorAll(".committee-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const details = button.nextElementSibling;
      const isExpanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!isExpanded));
      details.hidden = isExpanded;
      button.innerHTML = isExpanded
        ? 'View details <span aria-hidden="true">＋</span>'
        : 'Hide details <span aria-hidden="true">−</span>';
    });
  });

  const searchInput = document.querySelector("#resource-search");
  const categoryFilter = document.querySelector("#resource-filter");
  const resourceCards = [...document.querySelectorAll("[data-resource]")];
  const resourceCount = document.querySelector("#resource-count");
  const noResources = document.querySelector("#resource-empty");

  function filterResources() {
    if (!searchInput || !categoryFilter) return;
    const query = searchInput.value.trim().toLowerCase();
    const category = categoryFilter.value;
    let visible = 0;
    resourceCards.forEach((card) => {
      const matchesText = card.dataset.title.includes(query);
      const matchesCategory = category === "all" || card.dataset.category === category;
      const show = matchesText && matchesCategory;
      card.hidden = !show;
      if (show) visible += 1;
    });
    if (resourceCount) resourceCount.textContent = `${visible} ${visible === 1 ? "resource" : "resources"}`;
    if (noResources) noResources.hidden = visible !== 0;
  }

  searchInput?.addEventListener("input", filterResources);
  categoryFilter?.addEventListener("change", filterResources);

  const galleryButtons = [...document.querySelectorAll("[data-gallery-image]")];
  const lightbox = document.querySelector(".lightbox");
  if (lightbox && galleryButtons.length) {
    const lightboxImage = lightbox.querySelector("figure img");
    const lightboxCaption = lightbox.querySelector("figcaption");
    const closeButton = lightbox.querySelector(".lightbox-close");
    let activeIndex = 0;
    let priorFocus = null;

    const showPhoto = (index) => {
      activeIndex = (index + galleryButtons.length) % galleryButtons.length;
      const source = galleryButtons[activeIndex];
      lightboxImage.src = source.dataset.src;
      lightboxImage.alt = source.dataset.caption || "Conference photograph";
      lightboxCaption.textContent = source.dataset.caption || "";
    };

    const openLightbox = (index) => {
      priorFocus = document.activeElement;
      showPhoto(index);
      lightbox.classList.add("is-open");
      lightbox.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
      requestAnimationFrame(() => lightbox.classList.add("is-visible"));
      closeButton.focus();
    };

    const closeLightbox = () => {
      lightbox.classList.remove("is-visible");
      lightbox.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      window.setTimeout(() => lightbox.classList.remove("is-open"), 250);
      priorFocus?.focus();
    };

    galleryButtons.forEach((button, index) => button.addEventListener("click", () => openLightbox(index)));
    closeButton.addEventListener("click", closeLightbox);
    lightbox.querySelector(".lightbox-prev").addEventListener("click", () => showPhoto(activeIndex - 1));
    lightbox.querySelector(".lightbox-next").addEventListener("click", () => showPhoto(activeIndex + 1));
    lightbox.addEventListener("click", (event) => {
      if (event.target === lightbox) closeLightbox();
    });
    document.addEventListener("keydown", (event) => {
      if (!lightbox.classList.contains("is-open")) return;
      if (event.key === "Escape") closeLightbox();
      if (event.key === "ArrowLeft") showPhoto(activeIndex - 1);
      if (event.key === "ArrowRight") showPhoto(activeIndex + 1);
      if (event.key === "Tab") {
        const controls = [...lightbox.querySelectorAll("button")];
        const firstControl = controls[0];
        const lastControl = controls[controls.length - 1];
        if (event.shiftKey && document.activeElement === firstControl) {
          event.preventDefault();
          lastControl.focus();
        } else if (!event.shiftKey && document.activeElement === lastControl) {
          event.preventDefault();
          firstControl.focus();
        }
      }
    });
  }

  const scrollButton = document.querySelector(".scroll-top");
  if (scrollButton) {
    const updateScrollButton = () => scrollButton.classList.toggle("is-visible", window.scrollY > 500);
    window.addEventListener("scroll", updateScrollButton, { passive: true });
    updateScrollButton();
    scrollButton.addEventListener("click", () => {
      const behavior = window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";
      window.scrollTo({ top: 0, behavior });
    });
  }

  document.querySelectorAll("form[novalidate]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      const requiredFields = [...form.querySelectorAll("[required]")];
      const emailFields = [...form.querySelectorAll('input[type="email"]')];
      const phoneFields = [...form.querySelectorAll('input[type="tel"]')];
      const invalid = requiredFields.find((field) => !field.value.trim())
        || emailFields.find((field) => field.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value.trim()))
        || phoneFields.find((field) => {
          const digits = field.value.replace(/\D/g, "");
          return field.value && (digits.length < 7 || digits.length > 15);
        });
      form.querySelectorAll(".client-validation-error").forEach((message) => message.remove());
      form.querySelectorAll("[aria-invalid='true']").forEach((field) => field.removeAttribute("aria-invalid"));
      if (invalid) {
        event.preventDefault();
        invalid.setAttribute("aria-invalid", "true");
        const message = document.createElement("small");
        message.className = "field-error client-validation-error";
        message.textContent = !invalid.value.trim()
          ? "This field is required."
          : invalid.type === "email"
            ? "Enter a valid email address."
            : "Enter a phone number with 7 to 15 digits.";
        invalid.insertAdjacentElement("afterend", message);
        invalid.focus();
      }
    });
  });
})();
