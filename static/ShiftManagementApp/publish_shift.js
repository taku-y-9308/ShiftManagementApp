$(document).on('click','#open_publish_shift_modal',function () {
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"
    $('#publish_shift').modal('show');
    $('#submit_publish_shift').off('click');
    $('#submit_publish_shift').click(function(){
        let member = document.getElementById('submit-newshift-member').value;
        console.log(member);
        axios
            .post("/edit-shift/publish-shift/",{
                "publish_shift_start":$('#publish_shift_start').val(),
                "publish_shift_end":$('#publish_shift_end').val()
            })
            .then((res)=>{
                //alert('送信成功');
                $('#publish_shift').modal('hide');//modalを閉じる
            })
            .catch(()=>{
                alert('送信失敗しました');
            })
    })
  });