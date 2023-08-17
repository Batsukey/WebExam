document.addEventListener("DOMContentLoaded", function() {
    const profileContainer = document.querySelector(".profile-container");
    const dropdownContent = profileContainer.querySelector(".dropdown-content");

    profileContainer.addEventListener("mouseover", function() {
        dropdownContent.style.opacity = "1";
        dropdownContent.style.visibility = "visible";
        dropdownContent.style.pointerEvents = "auto";
    });

    profileContainer.addEventListener("mouseout", function() {
        dropdownContent.style.opacity = "0";
        dropdownContent.style.visibility = "hidden";
        dropdownContent.style.pointerEvents = "none";
    });
});
