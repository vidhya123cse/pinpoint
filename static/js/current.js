$(function () {
  $("#fileupload").change(function () {
      if (typeof (FileReader) != "undefined") {
          var dvPreview = $("#dvPreview");
          dvPreview.html("");
          var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.jpg|.jpeg|.gif|.png|.bmp)$/;
          $($(this)[0].files).each(function () {
              var file = $(this);
              if (regex.test(file[0].name.toLowerCase())) {
                  var reader = new FileReader();
                  reader.onload = function (e) {
                      var img = $("<img />");
                      img.attr("class", "img-fluid img-thumbnail");
                      img.attr("style", "height:100px;width: 100px; margin:10px");
                      img.attr("src", e.target.result);
                      dvPreview.append(img);
                  }
                  reader.readAsDataURL(file[0]);
              } else {
                  alert(file[0].name + " is not a valid image file.");
                  dvPreview.html("");
                  return false;
              }
          });
      } else {
          alert("This browser does not support HTML5 FileReader.");
      }
  });
});
  
function resetFile() {
  const file1 = document.getElementById("fileupload");
  const file2 = document.getElementById("dvPreview");
  file1.value = '';
  file2.value = '';
  $("#dvPreview").hide();
}
  



function resetvideo() {
  const file1 = document.getElementById("videobutton");
  file1.value = '';
  $("#up1").show();
  $("#up2").show();
  $("#up3").show();
  $("#video").hide();
  $("#third").hide();
  $("#live").hide();
}

function resetthird() {
  const file1 = document.getElementById("firstList");
  file1.value = '';
  $("#up1").show();
  $("#up2").show();
  $("#up3").show();
  $("#third").hide();
  $("#video").hide();
  $("#live").hide();
  document.getElementById("third").style.display = 'none';
  document.getElementById("firstList").required = false;
 
}


function resetlive() {
  $("#up1").show();
  $("#up2").show();
  $("#up3").show();
  $("#third").hide();
  $("#live").hide();
  $("#video").hide();
}













var htm = '';

function video()
{

htm = `
<div class="col-lg-12" style="margin-bottom: 10px;">
<div class=" col-xs-12 col-sm-6 col-md-9">
<div class="form-group" style = "margin-bottom: 10px;"><br>
<div style="margin: 20px;"><b>Upload Video</b></div>
          <div class="row col-xs-12 col-sm-6 col-md-9">
          <label class="custom-file">
          <input type="file" id ="videobutton" class="custom-file-input" name="videos" accept = ".mp4" multiple required/>
          <span class="custom-file-label" for="customFile">Choose file</span>
          </label>
          </div><br>
          <div class="row col-md-4 col-xs-12 col-sm-6 col-md-9">
          <input type="submit" name="action" id ="video" value="Upload" class="btn btn-primary pull-left" style="max-height:40px;min-width:200px;max-width: 200px;margin-top:9px; background-color:#2dc997; margin-bottom: 10px;" onclick="processing();" />
          &nbsp;<button type="button" class="btn btn-danger pull-left" style="min-width:200px;max-width: 200px; margin-bottom: 10px;" onclick="resetvideo()"> Reset The Field
          </button>
          </div>
          <br><br><br>
          </div>
</div>
</div>
`
document.getElementById("video").innerHTML= htm; 
document.getElementById("third").style.display = 'none';

}








function getauth(name)
{

document.getElementById(name).style.display = 'block';  
document.getElementById(name).required = true;
document.getElementById("date").required = true;
document.getElementById("starttime").required = true;
document.getElementById("endtime").required = true;



}


function live()
{

  htm = ` <div class="col-lg-12" style="margin-bottom: 10px;">
          <div class=" col-xs-12 col-sm-6 col-md-9">
          <div class="form-group" style = "margin-bottom: 10px;"><br>
          <div style="margin: 20px;"><b>Live Video Face Recogniton</b></div>
          <div class="row col-md-4 col-xs-12 col-sm-6 col-md-9">
            <input type="submit" name="action" id ="live" value="ON" class="btn btn-primary pull-left" style="max-height:40px;min-width:200px;max-width: 200px;margin-top:9px; background-color:#2dc997; margin-bottom: 10px;" onclick="liveprocessing();" />
          &nbsp;<button type="button" class="btn btn-danger pull-left" style="min-width:200px;max-width: 200px; margin-bottom: 10px;" onclick="resetlive()"> Reset The Field
          </button>
          </div>
          <br><br><br>
          </div>
</div>
</div>
  
  `
  document.getElementById("live").innerHTML= htm;
  document.getElementById("third").style.display = 'none';
}





function third()
{
document.getElementById("third").style.display = 'block';
document.getElementById("firstList").required = true;



}

$("#up1").click(function () {

  $("#up2").hide();
  $("#up3").hide();
  $("#third").hide();
  $("#live").hide();
  $("#video").show();
});

$("#up2").click(function () {

  $("#up1").hide();
  $("#up3").hide();
  $("#video").hide();
  $("#live").hide();
  $("#third").show();
});

$("#up3").click(function () {

  $("#up2").hide();
  $("#up1").hide();
  $("#third").hide();
  $("#video").hide();
  $("#live").show();
});
