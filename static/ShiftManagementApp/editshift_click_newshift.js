$(document).on('click','#create-newshift',function () {
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"
    $('#submit-newshift-modal').modal('show');
    $('#submit-newshift').off('click');
    $('#submit-newshift').click(function(){
        let member = document.getElementById('submit-newshift-member').value;
        console.log(member);
        axios
            .post("/edit-shift-Ajax/post-shiftdata/",{
                "id":null,
                "member":Number(member),
                "position":($('#position').val()),
                "date":$('#submit-newshift-date').val(),
                "start":$('#submit-newshift-start').val(),
                "end":$('#submit-newshift-end').val()
            })
            .then((res)=>{
                //alert('送信成功');
                $('#submit-newshift-modal').modal('hide');//modalを閉じる
                
            })
            .catch(()=>{
                alert('送信失敗しました');
            })
    })
  });