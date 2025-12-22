window.onload = function () {
    const horseSelect = document.getElementById("id_horse");
    const syndicateInput = document.getElementById("id_syndicate_name");

    if (horseSelect && syndicateInput) {
        horseSelect.addEventListener("change", function () {
            const selectedText =
                horseSelect.options[horseSelect.selectedIndex].text;
            if (selectedText && selectedText !== "---------") {
                const horseName = selectedText.split(" (")[0];
                syndicateInput.value = horseName + " Syndicate";
            }
        });
    }
};
