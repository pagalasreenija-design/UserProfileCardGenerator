// ---------- Live Image Preview ----------

const imageInput = document.getElementById("image");
const preview = document.getElementById("preview");

if (imageInput && preview) {
    imageInput.addEventListener("change", function () {

        const file = this.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
            };

            reader.readAsDataURL(file);
        }
    });
}


function downloadCard(cardId) {

    const card = document.getElementById(cardId);

    html2canvas(card, {
        backgroundColor: "#ffffff",
        scale: 3,
        useCORS: true
    }).then(function(canvas) {

        const link = document.createElement("a");

        link.download = "ProfileCard.png";
        link.href = canvas.toDataURL("image/png");

        link.click();

    });

}