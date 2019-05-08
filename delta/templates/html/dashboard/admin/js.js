var courses = [];


function reset_modal(user){
  $('.modal-body').empty()
  $('.modal-body').append('<div id="info">\
  <form id="edit-user-form" action="/dashboard/users/edit_user" class="form" style="border:1px solid grey;border-radius:5px;margin-bottom:10%">\
      <table>\
      <tr>\
      <td style="width:80%">\
         <div style="float:left" class="form-group col-md-6">\
           <label for="fn">Firstname</label>\
           <input type="text" name="fn" class="form-control" value="'+user.fields.first_name+'" disabled>\
           <label for="ln">Lastname</label>\
           <input type="text" name="ln" class="form-control" value="'+user.fields.last_name+'" disabled>\
         </div>\
         <div style="float:left" class="form-group col-md-6">\
         </div>\
         </td>\
        <td>\
       <img style="width:100%;height:auto" src="/media/'+user.fields.pic+'"\
       </td>\
       </tr></table>\
     <div id="details" style="margin:10px">\
       <div class="form-row">\
         <div class="form-group col-md-4">\
           <label for="em">E-mail</label>\
           <input type="text" name="em" class="form-control" value="'+user.fields.email+'" disabled>\
         </div>\
         <div class="form-group col-md-4">\
         </div>\
         <div class="form-group col-md-4">\
           <label for="us">Username</label>\
           <input type="text" name="us" class="form-control" value="'+user.fields.username+'" disabled>\
           <input type="hidden" name="us-fix" class="form-control" value="'+user.fields.username+'">\
         </div>\
       </div>\
         <div class="form-row">\
           <div class="form-group col-md-4">\
             <label for="ph">Phone</label>\
             <input type="text" name="ph" class="form-control" value="'+user.fields.phone+'" disabled>\
           </div>\
           <div class="form-group col-md-4">\
           </div>\
           <div class="form-group col-md-4">\
             <label for="mb">Mobile</label>\
             <input type="text" name="mb" class="form-control" value="'+user.fields.mobile+'" disabled>\
           </div>\
         </div>\
           <div class="form-row">\
             <div class="form-group col-md-4">\
               <label for="id">ID</label>\
               <input type="text" name="id" class="form-control" value="'+user.fields.idCode+'" disabled>\
             </div>\
             <div class="form-group col-md-4">\
             </div>\
             <div class="form-group col-md-4">\
               <label for="rl">Role</label>\
               <input type="text" name="rl" class="form-control" value="'+user.fields.role+'" disabled>\
             </div>\
           </div>\
           <div class="form-row">\
             <div class="form-group col-md-12">\
               <label for="ad">Address</label>\
               <input type="text" name="ad" class="form-control" value="'+user.fields.address+'" disabled>\
             </div>\
           </div>\
       </div>\
       <div>\
     </form>\
  </div>\
  <div id="tree"></div>\
  </div>')
  $('input').css('color','black')
  $(".modal-footer").empty()
  $(".modal-footer").append('<a type="button" class="btn btn-outline-primary waves-effect" data-dismiss="modal">Close</a>')
  $(".modal-footer").append('<a type="button" class="eClass btn btn-danger" style="color:white" href="/dashboard/users/'+user.fields.username+'/edit_user" id="edit">Edit Profile</a>')
  ready()
  $('#modal').modal();
}
function reset_course_modal(course,teacher,term,group){
  $('.modal-body').empty()
  $('.modal-header').empty()
  try {$('#edit').remove()} catch (e) {}
  $('.modal-header').append('<a class="cClass" href="/dashboard/course/'+ order({'code':course.fields.code,'group':group,'term':term}) +'"><h1>'+course.fields.course_name+'</h1></a>\
    <h5>Term: '+ term.season + " of "+term.year + ", Part "+ term.part +'</h5>')
  $('.modal-body').append('<div id="info">\
    <form class="form" method="post" style="border:1px solid grey;border-radius:5px;margin-bottom:10%">\
      <div style="margin:10px">\
       <div class="form-row">\
         <div class="form-group col-md-4">\
           <label for="fn">Teacher</label>\
           <input type="text" name="fn" class="form-control" value="'+teacher.fields.first_name+' '+teacher.fields.last_name+'" disabled>\
         </div>\
         <div class="form-group col-md-4">\
         </div>\
         <div class="form-group col-md-4">\
         <label for="ln" style="color:white">!</label>\
           <input name="ln" id="to-be-white" type="button" class="aClass btn btn-primary form-control" value="Teacher profile" href="/dashboard/users/'+teacher.fields.username+'">\
         </div>\
       </div>\
       </div>\
     </form>\
     <div class="" id="users">\
       <table class="table table-hover" id="course-user-list">\
       </table>\
     </div>')
  $('input').css('color','black')
}

function student_modal_creator(user,scores){
  reset_modal(user)
  $('#tree').treeview({data: scores});
  $('#centralModalSuccess').modal()
}
function teacher_modal_creator(user,courses){
  reset_modal(user)
  add_courses(courses)
  $('#centralModalSuccess').modal()
}
function staff_modal_creator(user){
  reset_modal(user)
}
function add_courses(courses){
  $('.modal-body').append('\
  <div id="course-container">\
  <a id="modal-courses" class="btn btn-primary btn-block" data-toggle="collapse" data-target="#collapseSemester" aria-expanded="true" aria-controls="collapseSemester"  href="#" >\
    <span data-feather="book"></span>\
    Show Courses\
  </a>\
  <div class="collapse" id="collapseSemester">\
    <ul id="year-courses-ul">\
    </ul>\
  </div></div>')

  var sina = courses
  if(typeof sina[0] == "undefined" )
    return
  var flag = sina[0]['term']['year']
  var count = 0
  for(var i=0;i<sina.length; i++){
    if(sina[i]['term']['year'] == flag && count==0){
      $('#year-courses-ul').append('<a id="collapseYearCover'+sina[i].term.year+'" class="nav-link" data-toggle="collapse" data-target="#collapseYear'+sina[i]['term']['year']+'" aria-expanded="true" aria-controls="collapseTerm" href="#" >\
        <li style="font-size:16px">'+sina[i]['term']['year']+'</li>\
      </a>\
      <div class="collapse" id="collapseYear'+sina[i]['term']['year']+'">\
        <ul class="list-group" id="year'+sina[i]['term']['year']+'">\
        </ul>\
      </div>')
      count++;
    }
    else if(sina[i]['term']['year'] != flag) {
    count = 0
     flag = sina[i]['term']['year']
     i--;
    }
  }
  flag = [sina[0]['term']['season'],sina[0]['term']['part']]
  count = 0
  for(var i=0;i<sina.length; i++){
    if(sina[i]['term']['season'] == flag[0] && sina[i]['term']['part'] == flag[1] && count==0){
      $('#year'+sina[i]['term']['year']).append('<li class="list-group-item" style="padding:0;margin:0 10px 0 0px;font-size:14px"><a id="'+sina[i].term.year+sina[i].term.season+sina[i].term.part+'" class="nav-link" data-toggle="collapse" data-target="#collapseTerm'+sina[i].term.year+sina[i]['term']['season']+sina[i]['term']['part']+'" aria-expanded="true" aria-controls="collapseTerm" href="#" >\
        '+sina[i]['term']['season'] + " Part " + sina[i]['term']['part']+'\
      </a>\
      <div class="collapse" id="collapseTerm'+sina[i].term.year+sina[i]['term']['season']+sina[i]['term']['part']+'">\
        <ul id="term'+sina[i]['term']['season']+sina[i]['term']['part']+'">\
        </ul>\
      </div></li>')
      count++;
    }
    else if(sina[i]['term']['season'] != flag[0] || sina[i]['term']['part'] != flag[1]) {
    count = 0
     flag = [sina[i]['term']['season'],sina[i]['term']['part']]
     i--;
    }
  }
  for(var i=0;i<sina.length; i++)
    $('#term'+sina[i]['term']['season']+sina[i]['term']['part']).append('<li style="font-size:12px"><a id="'+sina[i].term.year+sina[i].term.season+sina[i].term.part+sina[i].code+'" class="cClass nav-link" href="/dashboard/course/'+ order(sina[i]) +'">'+ sina[i].course_name +'</a></li>')
}
function order(input){
  var output = input.code +"_"+ input.group + "_"+ input.term.year + "_" + input.term.season + "_" + input.term.part
  return(output)
}

function course_modal_creator(data){
  var course = JSON.parse(data.course)[0]
  reset_course_modal(course,JSON.parse(data.teacher)[0],data.term,data.group)
    $('#to-be-white').css('color','white')
  var count = 0
  $('#course-user-list').append(
  '<tr>\
    <td style="background-color:grey;color:grey">!</td>\
    <td style="width:30%">Name</td>\
    <td style="width:20%%">Username</td>\
    <td style="width:15%">Mid Score</td>\
    <td style="width:15%">Final Score</td>\
    <td style="width:29%">Mobile</td>\
    <td style="width:10%">Activity</td>\
    <td style="width:10%">Profile</td>\
  </tr>')
  data.students.forEach(add_students)
  ready()

  $('#centralModalSuccess').modal()
}
function add_students(student,count){
  user = JSON.parse(student.user)[0]
  score = JSON.parse(student.score)[0]
  count += 1
  $('#course-user-list').append(
  '<tr>\
    <td>'+count+'</td>\
    <td style="width:30%">'+user.fields.first_name+' '+user.fields.last_name+'</td>\
    <td style="width:20%%">'+user.fields.username+'</td>\
    <td style="width:15%">'+score.fields.midScore+'</td>\
    <td style="width:15%">'+score.fields.finalScore+'</td>\
    <td style="width:29%">'+user.fields.mobile+'</td>\
    <td style="width:10%">'+(user.fields.is_active?'Active':'Deactive')+'</td>\
    <td style="width:10%"><a class="aClass" href="/dashboard/users/'+user.fields.username+'">Show</a></td>\
  </tr>')
}

function profile(addressValue){
    $.ajax({
      url: addressValue,
      method:'GET',
      success: function (data) {
        var user = JSON.parse(data.user)[0]
        if(user.fields.role == "Teacher")
          // console.log("teacher");
          teacher_modal_creator(user,data.courses)
        else if(user.fields.role == "Student")
          student_modal_creator(user,JSON.parse(data.scores.tree))
          // console.log("student");
        else
        staff_modal_creator(user)
        console.log("staff");
      },
      dataType: 'json'
    });
  }
function course_profile(addressValue){
      $.ajax({
        url: addressValue,
        method:'GET',
        dataType: 'json',
        success: function (data) {
          course_modal_creator(data)
        }
      });
    }
function query_courses(){
        $('#get-courses').ajaxForm({
        success: function (data) {
          var courses = data.courses
          $('#course-list').empty()
          var count = 0
          $('#course-list').append('<tr>\
            <th style="background-color:grey;color:grey;width:1%">!</th>\
            <th>Name</th>\
            <th>Code</th>\
            <th>Year</th>\
            <th>Season</th>\
            <th>Part</th>\
            <th>Group</th>\
            <th>Number of students</th>\
            <th>More Info</th>\
          </tr>')
          courses.forEach(fill_courses)
          ready()
        },
          dataType:'json',
      })
    }

function query_users(){
        $('#get-users').ajaxForm({
        success: function (data) {
          var users = JSON.parse(data.users)
          $('#user-list').empty()
          var count = 0
          $('#user-list').append('<tr>\
            <th style="background-color:grey;color:grey;width:1%">!</th>\
            <th>Name</th>\
            <th>Username</th>\
            <th>Role</th>\
            <th>Mobile</th>\
            <th>Status</th>\
            <th>Photo</th>\
            <th>Profile</th>\
          </tr>')
          users.forEach(fill_user)
          ready()
          },
          dataType:'json',
      })
  }
function fill_user(user,count){
    count += 1
    $('#user-list').append(
    '<tr>\
      <td>'+count+'</td>\
      <td style="width:30%">'+user.fields.first_name+' '+user.fields.last_name+'</td>\
      <td style="width:20%%">'+user.fields.username+'</td>\
      <td style="width:15%">'+user.fields.role+'</td>\
      <td style="width:29%">'+user.fields.mobile+'</td>\
      <td style="width:10%">'+(user.fields.is_active?'Active':'Deactive')+'</td>\
      <td style="width:10%"><img style="width:50%" src="/media/'+(user.fields.pic)+'"></td>\
      <td style="width:10%"><a class="aClass" href="/dashboard/users/'+user.fields.username+'">Show</a></td>\
    </tr>')

  }
function fill_courses(course,count){
    count += 1
    $('#course-list').append(
    '<tr>\
      <td>'+count+'</td>\
      <td style="width:20%">'+course.name+'</td>\
      <td style="width:15%">'+course.code+'</td>\
      <td style="width:10%">'+course.term.year+'</td>\
      <td style="width:15%">'+course.term.season+'</td>\
      <td style="width:10%">'+course.term.part+'</td>\
      <td style="width:10%">'+course.group+'</td>\
      <td style="width:10%">'+ course.num +'</td>\
      <td style="width:20%"><a class="cClass" href="/dashboard/course/'+ order(course) +'">Show</a></td>\
    </tr>')
  }
function ready(){
  $(document).ready(function(){
    $(".cClass").click(function(){
      var addressValue = $(this).attr("href");
      course_profile(addressValue)
      return false;
    });
  })
  $(document).ready(function(){
    $(".aClass").click(function(){
      var addressValue = $(this).attr("href");
      profile(addressValue)
      return false;
    });
  })
}

function save_edit(){
  $('#edit-user-form').ajaxForm({
  success: function (data) {
    submit_modal(data)
    $('#user-photo').attr('src',data.new_path)
    $('input[name=pic]').val('')
  },
    dataType:'json',
})
}

function submit_modal(data){
  $('.modal-body').empty()
  var check = data.status?'fa-check':'fa-times';
  var color = data.status?'green':'red';
  $('.modal-body').append('<i class="fas '+check+' fa-4x mb-3" style="color:'+color+'"></i>')
  $('.modal-body').append('<p>'+data.msg+'</p>')
  $('#modal').modal()
}

function submit_add_term_form(){
  $('#add-term-form').ajaxForm({
    success: function (data) {
      submit_modal(data);
      document.getElementById('add-term-form').reset()
    },
    dataType:'json',
  })
  console.log("double out")
}

function validate_username(){
    var username = $(this).val();
    if(username == "")
      $('#check_username').html("");
    else{
      $.ajax({
        url: address,
        data: {
          'username': username
        },
        method:'GET',
        dataType: 'json',
        success: function (data) {
          $('#check_username').html(data.msg);
          if(data.status)
             $('#check_username').css("color","green");
           else
             $('#check_username').css("color","red");
        }
      });
    }}

function submit_add_user_form(){
  $('#add-user-form').ajaxForm({
  success: function (data) {
    $('.text-center').empty()
    submit_modal(data)
    $('#check_username').html("");
  },
    dataType:'json',
})

}

function getCourses(){
  var term = $(this).val();
  $.ajax({
    url: get_course_address,
    data: {
      'info': term,
    },
    dataType: 'json',
    success: function (data) {
      $('#courses').prop('disabled',false)
      $('#courses').empty()
      $('#courses').append('<option value="" selected>Choose...</option>')
      for (var i of data.courses)
        $('#courses').append('<option>'+i.course_name+' - code:'+i.code+' - group:'+i.group+'</option>')
      courses = data.courses
    }
  });
}

function fill_teacher(){
    var course = $('#courses').val()
    course = course.split("-")
    course = [course[0].trim(),course[1].split(":")[1].trim(),course[2].split(":")[1].trim()]
    for (i of courses)
      if(i.course_name == course[0]&&i.code == course[1]&&i.group == course[2]){
        $('#teacherName').val(i.teacher.name)
        $('#teacherUsername').val(i.teacher.username)
      }
}

function validate_students(){
var names = $('#studentNames').val().split();
names = names[0].split('\n')
$.ajax({
  url: validate_students_address,
  data: {
    'info': names.join(),
  },
  dataType: 'json',
  success: function (data) {
    var flag = 0
    $('#studentsUsernames').empty()
    for(var i of data.response){
        if(i.status)
          $('#studentsUsernames').append('<li >'+ i.name + ' <span style="color:green">Valid</span></li>')
        else{
        $('#studentsUsernames').append('<li >'+ i.name + ' <span style="color:red">NOT Valid</span></li>')
        flag = 1;
      }
    }
    if(!flag&&$('#term').val()!="Choose..."&&$('#courses').val()!="Choose...")
      $('#submit').prop('disabled',false)
    else
      $('#submit').prop('disabled',true)
  }
});
}

function submit_student_to_course_form(){
  var names = $('#studentNames').val().split();
  names = names[0].split('\n')
  $('#student-to-course-form').ajaxForm({
    data : {
      'names':names
    },
    success: function (data) {
      submit_modal(data)
      document.getElementById('student-to-course-form').reset()
      $('#submit').prop('disabled',true)
      $('#studentsUsernames').empty()
      },
      dataType:'json',
  })
}

function submit_new_course_form(){
  $('#new-course-form').ajaxForm({
    success: function (data) {
    submit_modal(data)
    document.getElementById('new-course-form').reset()
    },
    dataType:'json',
  })
}

function submit_course_to_term_form(){
  $('#course-to-term-form').ajaxForm({
    success: function (data) {
    submit_modal(data)
    document.getElementById('course-to-term-form').reset()
    },
    dataType:'json',
  })
}

function fill_teacherName(){
  $('#teacherUsername').css("color","black");
  var teacherUsername = $(this).val();
  if(teacherUsername == ""){
    $('#teacherName').val("");
    $('#teacherName').css("color","black");
  }
  else{
  $.ajax({
    url: autofill,
    data: {
      'info': teacherUsername,
      'wanted':"teacherName"
    },
    dataType: 'json',
    success: function (data) {
      if(data.status){
        $('#teacherName').val(data.info);
         $('#teacherName').css("color","green");
       }
       else{
         $('#teacherName').val("");
         $('#teacherName').attr("placeholder",data.info);
       }
    }
})
}}
function fill_courseCode(){
  $('#courseName').css("color","black");
  var courseName = $(this).val();
  if(courseName == ""){
    $('#courseCode').val("");
    $('#courseCode').css("color","black");
  }
  else{
  $.ajax({
    url: autofill,
    data: {
      'info': courseName,
      'wanted':"courseCode"
    },
    dataType: 'json',
    success: function (data) {
      if(data.status){
        $('#courseCode').val(data.info);
         $('#courseCode').css("color","green");
       }
       else{
         $('#courseCode').val("");
         $('#courseCode').attr("placeholder",data.info);
       }
    }
  });
}}
function fill_courseName(){
  $('#courseCode').css("color","black");
  var courseCode = $(this).val();
  if(courseCode == ""){
    $('#courseName').val("");
    $('#courseName').css("color","black");
  }
  else{
  $.ajax({
    url: autofill,
    data: {
      'info': courseCode,
      'wanted':"courseName"
    },
    dataType: 'json',
    success: function (data) {
      if(data.status){
        $('#courseName').val(data.info);
         $('#courseName').css("color","green");
       }
       else{
         $('#courseName').val("");
         $('#courseName').attr("placeholder",data.info);
       }
    }
})
}}
function fill_teacherUsername(){
  $('#teacherName').css("color","black");
    var teacherName = $(this).val();

    if(teacherName == ""){
      $('#teacherUsername').val("");
      $('#teacherUsername').css("color","black");
    }
    else{
    $.ajax({
      url: autofill,
      data: {
        'info': teacherName,
        'wanted':"teacherUsername"
      },
      dataType: 'json',
      success: function (data) {
        if(data.status){
          $('#teacherUsername').val(data.info);
           $('#teacherUsername').css("color","green");
         }
         else{
           $('#teacherUsername').val("");
           $('#teacherUsername').attr("placeholder",data.info);
         }
      }
  })
}}
