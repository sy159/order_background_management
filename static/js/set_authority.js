$("#body").on('click','input',function () {
             var clsn=this.className;
             if(clsn=='all'){
                 if ($('.all').prop("checked")) {
                     $('.father_menu, .child_menu').prop('checked', true);
                 } else {
                     $('.father_menu, .child_menu').prop('checked', false);
                 }
             }else if(clsn.indexOf('father_menu') > 0){
                 var fid = parseInt($(this).val());
                 if ($(this).prop("checked")) {
                     $('.child_menu_' + fid).prop('checked', true);
                 } else {
                     $('.child_menu_' + fid).prop('checked', false);
                 }
                 var flen=$('.father_menu').length;

                 var i=0;
                 $('.father_menu').each(function () {
                     if ($(this).prop('checked')) {
                         i++;
                     }
                 });
                 if(flen==i){
                     $("#all").prop('checked',true);
                 }else {
                     $("#all").prop('checked',false);
                 }
             }else if(!clsn.indexOf('child_menu')){
                 var fid = $(this).attr('data-fid');
                 if ($(this).prop("checked")) {
                     $('.menu_' + fid).prop('checked', true);
                 } else {
                     var flag = false;
                     $('.child_menu_' + fid).each(function(){
                         if ($(this).prop('checked')) {
                             flag = true;
                         }
                     });
                     $('.menu_' + fid).prop('checked', flag);
                 }
             }

         });//权限勾选