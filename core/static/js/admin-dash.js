$(document).ready(function(){
    $.getJSON('/users/', function(data){
        $('#users').html('');
        renderUsers($('#users'), data);
    });

    //utility for displaying list of users
    function renderUsers(el, users){
        $.each(users, function(key, user){
            el.append(
                '<tr><td>' + (parseInt(key, 10) + 1) + '</td>' +
                     '<td>' + user.first_name + '</td>' +
                     '<td>' + user.last_name + '</td>' +
                     '<td>' + user.username + '</td>' +
                     '<td>' + user.position + '</td>' +
                     '<td><span class="fa fa-info-circle" id="' + user.url + '" ></span></td>' +
                '</tr>'
            );
        });
    };

    // perform get detail
    $(document).on('click', 'span', function(){
        getDetail($(this).attr('id'));
    });

    // get detail
    function getDetail(url){
        $.getJSON(url, function(data){
            //render User details here
            $('#list').hide();
            $('#detail').html('');
            $('#detail').show();
            renderDetail($('#detail'), data);
        });
    };

    // utility to render user details

    function renderDetail(el, user){
        el.append(
            '<div class="row align-item-center justify-content-center">' +
                '<div class="col-md-6">' +
                    '<div class="card"><img class="card-img" src="' + user.picture + '" alt="Card image"></div>' +
                    '<div class="row col-md-12">' +
                        '<h1>' + user.first_name + '   ' + user.last_name + '</h1><br>' +
                    '</div>' +
                '</div>' +
            '</div>'

        );
    };

    // Search
    $('#search').on('click', function(){
        var q = $('input[name="q"]').val();
        $.getJSON('/search/?q=' + q, function(data){
            $('#list').show();
            $('#detail').hide();
            $('#users').html('');
            renderUsers($('#users'), data);
        });
    });
});