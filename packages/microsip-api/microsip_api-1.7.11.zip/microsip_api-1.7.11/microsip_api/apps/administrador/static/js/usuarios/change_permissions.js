function cambia_permiso(permiso_id, checked)
{
  var django_user_id = $("#django_user_id").val();
  $.ajax({
    url:'/administrador/change_user_permission/',
    type : 'get',
    data:{
      'permiso_id' : permiso_id,
      'django_user_id': django_user_id,
      'checked':checked
    },
    error: function() {
      alert('algo fallo');
    },
  });
}

$.ajax({
  url:'/administrador/get_apppsermissions/',
  type : 'get',
  data:{'username': $("#django_username").val()},
  success: function (data) {
    $("#permissions").jstree({
      "core" : {
          "themes" : {
            "variant" : "small"
          },
          'data' : data,
        },
       "types" : {
          "default" : {
            "icon" : "glyphicon glyphicon-co"
          },
          "demo" : {
            "icon" : "glyphicon glyphicon-co"
          }
        },
       "plugins" : ["checkbox", "types",]
     }).on('select_node.jstree', function (e, data) {
        if ($.isNumeric(data.node.id)){
          cambia_permiso(data.node.id, true);
        }
    }).on('deselect_node.jstree', function (e, data) {
        if ($.isNumeric(data.node.id)){
          cambia_permiso(data.node.id, false);
        }
    });
  },
  error: function() {
    alert('algo fallo');
  },
});

$(".permiso_chbox").on('change', cambia_permiso);