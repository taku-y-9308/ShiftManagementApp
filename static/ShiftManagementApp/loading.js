//読込中画面の表示
function dispLoading(msg){
    if (msg == undefined){
        msg = "";
    }
    let dispmsg = '<span class="sr-only">Loading...</span>';

    //ローディング画面がまだ表示されてない場合のみ実行
    if($('#loading').length == 0){
        $('body').append('<div id="loading" class="spinner-border text-primary" role="status">'+dispmsg+'</div>');   
    }
}
//読込中画面の非表示
function removeLoading(){
    $('#loading').remove();
}