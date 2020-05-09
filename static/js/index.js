
var htm = '';

/*emailField.addEventListener('keyup', function (event) {
	isValidEmail = emailField.checkValidity();
	
	if ( isValidEmail ) {
	  okButton.disabled = false;
	} else {
	  okButton.disabled = true;
	}
  });
	
  okButton.addEventListener('click', function (event) {
	signUpForm.submit();
  });
*/
$("#captche").hide();
function codevalidate(){

	var v = grecaptcha.getResponse()
	console.log(v.length);
	if (v.length == 0){

		document.getElementById("captche").innerHTML = "Captcha code empty";
		$("#captche").show();
		return false;
	}
	else
	{
		$.post("/login");
		$("#captche").hide();
		signin.submit();
	}
	
}


var check = function() {
	if (document.getElementById('password').value ==
	  document.getElementById('confpassword').value) {
	  document.getElementById('message').style.color = 'green';
	  document.getElementById('message').innerHTML = 'matching';
	} else {
	  document.getElementById('message').style.color = 'red';
	  document.getElementById('message').innerHTML = 'not matching';
	}
  }

function showfield(name)
{
    if(name=='Other'){
		document.getElementById('dep').style.display="block";
		document.getElementById("dep").required = true;
	}
    else{ 
		document.getElementById('dep').style.display="none";
		document.getElementById("dep").required = false;
	}
}
					






function User()
{


htm = `
<h2 class="well" style="min-width: 320px;margin-top:2%; text-align: center;font-weight: bold;"id ="register" >Registration Form</h2>
<form action ="/register" method ="POST" enctype="multipart/form-data">
<div class="col-lg-12 ">
<div class=" col-xs-12 col-sm-6 col-md-9">


			<div class="row">
			<div class="col-xs-12 col-sm-6 form-group">
			<label><b>First Name &nbsp;<span style="color: red;">*</span></b></label>
			<input type="text" name="firstname" placeholder="Enter First Name" class="form-control" value="" pattern="([a-zA-Z]*)" title="It contains alphabets only"  required />
			</div>


			<div class="col-xs-12 col-sm-6 form-group">
			<label><b>Last Name &nbsp;<span style="color: red;">*</span></b></label>
			<input type="text" placeholder="Enter Last Name" name="lastname" class="form-control" value="" pattern="([a-zA-Z]*)" title="It contains alphabets only"  required />
			</div>
			</div>					


			<div class="row">
			<div class="col-xs-12 col-sm-6 col-md-9 form-group">
			<label><b>User Name &nbsp;<span style="color: red;">*</span></b></label>
			<input type="text" name="username" placeholder="Enter User Name " class="form-control" value="" pattern="([0-9a-zA-Z]*)" title="It contain letters and numbers only"  required/>
			</div>
			</div>
			
			<div class="row">
			<div class="col-xs-12 col-sm-6 form-group">
			<label><b>Password &nbsp;<span style="color: red;">*</span></b></label>
			<input type="password" id = "password" name="password" placeholder="Enter Password *"  class="form-control"  maxlength="12"  pattern="[0-9a-zA-Z].{8,}" title="It includes  numbers , uppercase,lowercase letter, and at least 8 or more characters required (Max length:12)"   onkeyup=" check();" required >
			</div>	
			

			
			<div class="col-sm-6 form-group">
			<label><b>Confirm password &nbsp;<span style="color: red;">*</span></b></label>
			<input type="password" id = "confpassword" name="confpassword" placeholder="Enter Confirm Password *" class="form-control" value=""  maxlength="12" pattern="[0-9a-zA-Z].{8,}" title="It includes  numbers , uppercase,lowercase letter, and at least 8 or more characters required (Max length:12)" onkeyup="check();"  required >
			<span id='message'></span>
			</div>	
			</div>	
	
			<div class="row">					
			<div class="col-sm-4 form-group col-xs-12 col-sm-6 ">
			<label><b>Mobile Number &nbsp;<span style="color: red;">*</span></b></label>
			<input type="tel" name="mobile" placeholder="Enter Mobile Number *" class="form-control" value=""  maxlength="10" pattern="[0-9]{10}" title="10 digit number" required />	</div>


			<div class="form-group col-sm-4 col-xs-12 col-sm-6 ">
			<label><b>Email Address &nbsp;<span style="color: red;">*</span></b></label>
			<input type="email" name="mail" placeholder="Enter Email Address *" class="form-control" title="Valid email address" required />
			</div>	

			</div>

			<div class = "row">
			<div class="form-group col-xs-12 col-sm-6">
			<label><b>Address &nbsp;<span style="color: red;">*</span></b></label>
			<textarea name="address" placeholder="Enter Address Here.." rows="3" class="form-control"  title="It contains Alphabets and Numbers only"  required/></textarea>
			</div>	
			
			<div class="col-sm-4 form-group col-xs-12 col-sm-6">
			<label><b>State &nbsp;<span style="color: red;">*</span></b></label>
			<select id="list" name="state" onclick="selct_district(this.value)" class="form-control" required >
			<option value ="">--Select State--</option>
			<option value ="Andhra Pradesh">Andhra Pradesh</option>
			<option value ="Arunachal Pradesh">Arunachal Pradesh</option>
			<option value ="Assam">Assam</option>
			<option value ="Bihar">Bihar</option>
			<option value ="Chhattisgarh">Chhattisgarh</option>
			<option value ="Dadra and Nagar Haveli">Dadra and Nagar Haveli</option>
			<option value ="Daman and Diu">Daman and Diu</option>
			<option value ="Delhi">Delhi</option>
			<option value ="Goa">Goa</option>
			<option value ="Gujarat">Gujarat</option>
			<option value ="Haryana">Haryana</option>
			<option value ="Himachal Pradesh">Himachal Pradesh</option>
			<option value ="Jammu and Kashmir">Jammu and Kashmir</option>
			<option value ="Jharkhand">Jharkhand</option>
			<option value ="Karnataka">Karnataka</option>
			<option value ="Kerala">Kerala</option>
			<option value ="Madhya Pradesh">Madhya Pradesh</option>
			<option value ="Maharashtra">Maharashtra</option>
			<option value ="Manipur">Manipur</option>
			<option value ="Meghalaya">Meghalaya</option>
			<option value ="Mizoram">Mizoram</option>
			<option value ="Nagaland">Nagaland</option>
			<option value ="Orissa">Orissa</option>
			<option value ="Puducherry">Puducherry</option>
			<option value ="Punjab">Punjab</option>
			<option value ="Rajasthan">Rajasthan</option>
			<option value ="Sikkim">Sikkim</option>
			<option value ="Tamil Nadu">Tamil Nadu</option>
			<option value ="Telangana">Telangana</option>
			<option value ="Tripura">Tripura</option>
			<option value ="Uttar Pradesh">Uttar Pradesh</option>
			<option value ="Uttarakhand">Uttarakhand</option>
			<option value ="West Bengal">West Bengal</option>
			</select>
			</div>	
			</div>

			<div class = "row">
			<div class="col-sm-4 form-group col-xs-12 col-sm-6 ">
			<label><b>City &nbsp;<span style="color: red;">*</span></b></label>
			<select id='secondlist' name="city" class="form-control" required >
			<option value="">--Select City--</option>
			</select>
			</div>	


			<div class="col-sm-4 form-group col-xs-12 col-sm-6 ">
			<label><b>Zip &nbsp;<span style="color: red;">*</span></b></label>
			<input type="text" name="zipcode" placeholder="Enter Zip Code Here.." class="form-control" pattern="[0-9]{6}" title="It contains 6 digits only" maxlength="6" required  />
			</div>
			</div>		
					
			<div class="row">
			<div class="form-group"><br>
			<label class=" control-label" for="filebutton"><b>Upload Any proof &nbsp;<span style="color: red;">*</span></b></label>
			<div class="col-xs-12 col-sm-6 col-md-9">
			<input name="idproof" class="input-file" id="filebutton" type="file" accept=".jpg,.jpeg,.pdf,.png" required>
			</div>
			</div>
			</div>
		</div>
	</div>

					<br>
						<div class="col-sm-4 container-fluid col-xs-12 col-sm-6"style="margin:auto auto auto auto; min-width: 300px; max-width: 85%; border-radius: 7%;"><br>
		  <label><b style="font-size: 27px;">Instructions</b></label>
		  <br>
		  <ul style="text-align:left">
		  <li>Use this site for good and legal things only.Malpractises should be avoided.</li>
		  <li>The input image you uploaded should  be clear. Noisy or incorrect image should lead to incorrect result. That willl not be our fault.</li>
		  <li>All the information given should be correct and not illegaly created.</li>
		  <li>Creating fake missing cases and use this site for search that person is a crime.</li>
		  <li>Your personal information is completely encrypted and safe in our hand.</li>
		  </ul>
		<br>
		<br>
		</div> 
		<input type="checkbox" class="form-check-input position-static" id="userinstruct" value="done" required>
		&nbsp;<label class="form-check-label"> I have a Read the Instructions</label> &nbsp;<span style="color: red;">*</span><br><br><br>
		  
		 <br><br>
		 <span style="color: red;">* Required Fields</span><br><br>
		
						<button type="submit" id ="usersignup" style=" background-color:#2dc997;max-width: 50%;" class="btn btn-lg btn-info">Submit</button>	<br>
						</form>
						
  
						`

document.getElementById("user").innerHTML= htm;

}














function Authority()
{


htm = `<h2 class="well" style="min-width: 320px;margin-top:2%; text-align: center;font-weight: bold;"id ="authority" >Registration Form</h2>
<form action="/reg_official" method = "POST"  enctype="multipart/form-data">
<div class="col-lg-12 ">
<div class=" col-xs-12 col-sm-6 col-md-9">

						<div class="row">
						<div class="col-xs-12 col-sm-6 form-group">
							<label><b>First Name &nbsp;<span style="color: red;">*</span></b></label>
							<input type="text" placeholder="Enter First Name" name="fname" class="form-control" value="" pattern="([a-zA-Z]*)" title="It contains alphabets only"  required />
						</div>
						<div class="col-xs-12 col-sm-6 form-group">
							<label><b>Last Name &nbsp;<span style="color: red;">*</span></b></label>
							<input type="text" placeholder="Enter Last Name"  name="lname" class="form-control" value="" pattern="([a-zA-Z]*)" title="It contains alphabets only"  required />
						</div>
						</div>			
						<div class="row">

						<div class="col-xs-12 col-sm-6 col-md-9 form-group">
						<label><b>User Name &nbsp;<span style="color: red;">*</span></b></label>
						<input type="text" placeholder="Enter User Name "  name="uname" class="form-control" value="" pattern="([0-9a-zA-Z]*)" title="It contain letters and numbers only"  required />
						</div>
						</div>
				
						<div class="row">
						<div class="col-xs-12 col-sm-6 form-group">
						<label><b>Password &nbsp;<span style="color: red;">*</span></b></label>
						<input type="password" id = "password" name="password" placeholder="Enter Password *"  class="form-control"  maxlength="12"  pattern="[0-9a-zA-Z].{8,}" title="It includes  numbers , uppercase,lowercase letter, and at least 8 or more characters required (Max length:12)"   onkeyup=" check();" required >
						</div>	
						
			
						
						<div class="col-sm-6 form-group">
						<label><b>Confirm password &nbsp;<span style="color: red;">*</span></b></label>
						<input type="password" id = "confpassword" name="confpassword" placeholder="Enter Confirm Password *" class="form-control" value=""  maxlength="12" pattern="[0-9a-zA-Z].{8,}" title="It includes  numbers , uppercase,lowercase letter, and at least 8 or more characters required (Max length:12)" onkeyup="check();"  required >
						<span id='message'></span>
						</div>	
						</div>	
				

						<div class="row">					
						<div class="col-sm-4 form-group col-xs-12 col-sm-6 ">
						<label><b>Mobile Number &nbsp;<span style="color: red;">*</span></b></label>
						<input type="tel" name="mobile" placeholder="Enter Mobile Number *" class="form-control" value=""  maxlength="10" pattern="[0-9]{10}" title="10 digit number" required >	</div>


						<div class="form-group col-sm-4 col-xs-12 col-sm-6 ">
						<label><b>Email Address &nbsp;<span style="color: red;">*</span></b></label>
						<input type="email" name="email" placeholder="Enter Email Address *" class="form-control" required>
						</div>	
						</div>

						<div class="row">
						<div class="form-group col-sm-4 col-xs-12 col-sm-6">
						<label for="job">Job Title:</label>&nbsp;

						<select id="job" name="job" onclick="showfield(this.value)" required>
						  <option class="dropdown-item" value="">--select option--</option>
						  <option class="dropdown-item" value="Police">Police Force</option>
						  <option class="dropdown-item" value="RPF">RPF</option>
						  <option class="dropdown-item" value="Other">Other</option>
						
						</select>
						</div>


						 <div class="form-group col-sm-4 col-xs-12 col-sm-6 ">
					  
						 <input style="display:none;" type="text" class="form-control" placeholder='input department' id='dep' name='department'>
					
						 </div>

						
				
					<div class="form-group"><br>
					<label class=" control-label" for="filebutton"><b><span style="color: red;">*</span>Upload ID card Image</b></label>
					<div class="col-xs-12 col-sm-6 col-md-9">
					<input name="jobproof" class="input-file" id="filebutton" type="file" required>
					</div>
					</div>
					</div>


</div>
</div>
<div class="col-sm-4 form-group col-xs-12 col-sm-6"style="	margin:auto auto auto auto; min-width: 300px; max-width: 85%; border-radius: 7%;"><br>
<label><b style="font-size: 27px;">Instructions</b></label>
<br>
<ul style="text-align:left">
<li>Use this site for good and legal things only.Malpractises should be avoided.</li>
<li>The input image you uploaded should  be clear. Noisy or incorrect image should lead to incorrect result. That willl not be our fault.</li>
<li>All the information given should be correct and not illegaly created.</li>
<li>Creating fake missing cases and use this site for search that person is a crime.</li>
<li>Your personal information is completely encrypted and safe in our hand.</li>
</ul>
<br>
<br>
</div> 
<input type="checkbox" class="form-check-input position-static" id="instruct" value="done" required>
&nbsp;<label class="form-check-label"> I have a Read the Instructions</label>&nbsp;<span style="color: red;">*</span><br><br><br>

<br><br>
<span style="color: red;">* Required Fields</span><br><br>

			  <button type="submit" name="submit" style="background-color:#2dc997;max-width: 50%;" class="btn btn-lg btn-info">Submit</button>	<br>
	
			  </form>
			  `

document.getElementById("authority").innerHTML= htm;

}

$("#but1").click(function () {

	$("#but1").hide();
	$("#but2").hide();
	$("#authority").hide();
	$("#user").show();

});

$("#but2").click(function () {

	$("#but1").hide();
	$("#but2").hide();
	$("#user").hide();
	$("#authority").show();
	
});


$("#but4").click(function () {

	$("#but1").show();
	$("#but2").show();
	$("#authority").hide();
	$("#user").hide();
	

});


