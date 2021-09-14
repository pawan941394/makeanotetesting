var options = {
  placeholder: "Waiting for your precious content",
  theme: "snow",
};

var editor = new Quill("#quillEditor", options);
//   var preciousContent = document.getElementById('myPrecious');
//   var justTextContent = document.getElementById('justText');
// var justHtmlContent = document.getElementById("justHtml");

editor.on("text-change", function () {
  // var delta = editor.getContents();
  // var text = editor.getText();
  // preciousContent.innerHTML = JSON.stringify(delta);
  // justTextContent.innerHTML = text;
  // justHtmlContent.innerHTML = justHtml;
  // justHtmlContent.value = justHtml;
  var justHtml = editor.root.innerHTML;
  console.log(justHtml);
  document.getElementById("justHtml").value = justHtml;
});
