$(document).ready(function(){
    // get user detail from backend
    // ths #user contains the user-detail endpoint
    var user = $("#user").text();
    $.getJSON(user, function(data){
      skills = data.skills;
      interest = data.interest;
      if (skills && skills.length){
        renderSkills($('#skills-list'), skills);
        renderInterest($("#interest"), interest);
      };
    // set the form element to the user's current value/state
    $("input[name='skills']").attr('value', JSON.stringify(skills));
    $("input[name='interest']").attr('value', JSON.stringify(interest));
    });

    //to add interest
    $('#addInterest').on('click', function(){
      var $interest = $("#interest"),
          $interestForm = $('#interestForm');
      $interestForm.html('<input type="text" id="intF"><span id="doneInt" class="fa fa-check"></span>');
    });

    // done with interest
    $(document).on('click', '#doneInt', function(){
      var intrst = $('#intF').val();
      $('#intF').val('');
      interest.push(intrst);
      $("#interest").html('');
      renderInterest($("#interest"), interest);
      $("input[name='interest']").attr('value', JSON.stringify(interest));
      console.log($("#interest"));
    });

    // utility to render interests
    function renderInterest(el, interest){
      $.each(interest, function(key, val){
        el.append('<span class="badge badge-pill badge-primary">' + val + '</span>')
      });
    };

    //to start adding skills
    $("#addSkill").on('click', function(){
        renderSkillForm($('#skillForm'));
    });

    // to add more skills
    $(document).on('click', '#add', function(){
      var title = $('#title').val(),
          level = $('#level').val();
      // validation such as type checking could be added here
      if(title && level){
        skills.push({'title':title, 'level':level});
      };
      $("input[name='skills']").attr('value', JSON.stringify(skills));
      renderSkills($('#skills-list'), skills);
      renderSkillForm($('#skillForm'));
    });

    // to end skill addition
    $(document).on('click', '#done', function(){
      var title = $('#title').val(),
          level = $('#level').val();
      // validation such as type checking could be added here
      if(title && level){
        skills.push({'title':title, 'level':level});
      };
      $('#skillForm').html('');
      renderSkills($('#skills-list'), skills);
      $("input[name='skills']").attr('value', JSON.stringify(skills));
    });

    // trigger the file input field when the camera icon is clicked
    $("#upload").click(function () {
      $("input[type='file']").trigger('click');
    });

    // preview uploaded picture
    $('input[type="file"]').on('change', function() {
      $("img").attr('src', URL.createObjectURL($(this)[0].files[0]));
    });

    // utility to render skills in a table
    function renderSkills(el, iterable){
      el.html('');
      $.each(iterable, function(key, val){
        el.append('<tr><td>' + val.title + '</td><td>' + val.level + '</td><td><span class="fa fa-trash" id="delete" key="' + key + ' "></span></td></tr>');
      });
    };

    // utility to render skill form
    function renderSkillForm(el){
      el.html(
        '<div class="col-md-4 form-group"><input type="text" name="title" class="form-control" id="title"></div>' +
        '<div class="col-md-4 form-group"><input type="number" max="100" min="20" name="level" class="form-control" id="level"></div>' +
        '<div class="col-md-4"><span class="fa fa-plus btn btn-primary" id="add"></span><small>Click either of these before updating</small><span class="fa fa-check btn btn-primary pull-right" id="done"></span>'
      );
    };

    // delete or remove skill, takes the index of element, skills array and the table element to render the skills
    function deleteSkill(k, arr, el){
      arr.splice(k, 1);
      renderSkills(el, arr);
    };

    $(document).on('click', 'span#delete', function(){
      var key = $(this).attr('key');
      if (key){
        deleteSkill(key, skills, $('#skills-list'));
        $("input[name='skills']").attr('value', JSON.stringify(skills));
      };
    });
});