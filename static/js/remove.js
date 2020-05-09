var htm = '';
  
  function myDIV()
  {
  
  htm = `
 
  <ul class="list-group"></ul>
  <li class="list-group-item"> {{user.fname}}</li>
    <li class="list-group-item">{{user.lname}}</li>
      <li class="list-group-item">{{user.phone}}</li>
 </ul>

  `
  document.getElementById("myDIV").innerHTML= htm; 
  
  }
  
  
  
  
  
  
  
  
  function getauth(){
  
  var list1 = document.getElementById('firstList').value;
  var list2 = document.getElementById("secondList");
  
  
  if (list1 =='1')
  {
  
  list2.options.length=0;
  list2.options[0] = new Option('--Select--', '');
  list2.options[1] = new Option('Ernakulam Junction South (ERS)', '1');
  list2.options[2] = new Option('Thiruvananthapuram Central Station (TVC)', '2');
  list2.options[3] = new Option('Ernakulam Town Station (ERN)', '3');
  list2.options[4] = new Option('Angamaly Station (AFK)', '4');
  list2.options[5] = new Option('Chalakudi Railway Station (CKI)', '5');
  
  
  }
  else if (list1 =='2')
  {
  
  list2.options.length=0;
  list2.options[0] = new Option('--Select--', '');
  list2.options[1] = new Option('Police Stations-THiruvanthapuram','');
  list2.options[2] = new Option('kollam', '');
  list2.options[3] = new Option('Pathanamthitta', '');
  list2.options[4] = new Option('alappuzha', '');
  list2.options[5] = new Option('Kottayam', '');
  
  }
  }
  
  
  
  
  function third()
  {
  htm = `
  
  <centre>
  <div class="col-md-4" id ="mass">
  <form action="" method="POST" >
  <h4>Select Department</h4>
  <div class ="container-fluid">
  <select class="form-control"  id='firstList' name='firstList' onclick="getauth()" required>
  <option class="dropdown-item" value="0">--Select--</option>
                            <option class="dropdown-item" value="1">Railways</option>
                            <option class="dropdown-item" value="2">Police</option>
                            
  </select>
   
  <h4>Locate here</h4>
  <select class="form-control"  id='secondList' name='secondList' required >
  </select>
  </div><br><br>
  
  <div class ="row col-md-4 col-xs-12 col-sm-6 col-md-9"style="margin-left:5px;">
  <button type="submit" class="btn btn-primary pull-left" style="max-width: 200px;margin-left: 10px; background-color:#2dc997; margin-bottom: 10px;"> Request for Video</button>
  <button type="button" class="btn btn-danger pull-left" style="max-width: 200px;margin-left: 10px; margin-bottom: 10px;" onclick="resetthird()"> Reset The Field
            </button>
          </div>
   <br><br><br>
  </form>
  </div>
  
  <br><br>
  </centre>
  
  
  
  `
  document.getElementById("third").innerHTML= htm;
  
  }
  
  $("#up1").click(function () {
  
      $("#up2").hide();
    $("#third").hide();
    $("#video").show();
  });
  
  $("#up2").click(function () {
  
      $("#up1").hide();
    $("#video").hide();
    $("#third").show();
  
      
  
  });