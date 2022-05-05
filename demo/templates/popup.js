document.addEventListener('DOMContentLoaded', () => {
   var y = document.getElementById("index_link");
   y.addEventListener("click", openIndex);
});

function openIndex() {
   chrome.tabs.create({active: true, url: "http://127.0.0.1:8000/search_form/"});
}