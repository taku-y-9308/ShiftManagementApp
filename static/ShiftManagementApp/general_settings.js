window.addEventListener('DOMContentLoaded',general_settings)

function general_settings(){
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"
    dispLoading('Loading...');
    //post_dataをnullで渡すと画面読み込み時に必要な情報が帰ってくる
    axios
        .post('/general-settings/',{
            'post_data_type': null
        })
        .then((res)=>{
            console.log(res);
            const shop_id_El = document.getElementById('shop_id');
            const username_El = document.getElementById('username');
            const email_El = document.getElementById('email')

            shop_id_El.value = res.data.shop_id;
            username_El.value = res.data.username;
            email_El.value = res.data.email;

            //管理ユーザーの場合はシフト締め切りも表示する
            if(res.data.deadline != 'undefined'){
                const deadline_El = document.getElementById('deadline');
                deadline_El.value = res.data.deadline + '日';
            }
        })
        .catch((res)=>{
            console.log(res);
        })
        .finally(()=>{
            removeLoading();
        })
}

function change_username(){
    $('#change_username').modal('show');
    $('#submit_modified_username').off('click')
    $(('#submit_modified_username')).click(function(){
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
        axios.defaults.xsrfCookieName = "csrftoken"
        dispLoading('Loading...');
        axios
            .post('/general-settings/',{
                'post_data_type': 'modified_username',
                'modified_username': $('#modified_username').val()
            })
            .then((res)=>{
                if(res.data.res_code == 0){
                    $('#change_username').modal('hide');
                    general_settings();
                    $('#successful_modification_modal').modal('show');
                }else{
                    alert('error')
                }
            })
            .catch((res)=>{
                console.log('error'+res);
            })
            .finally(()=>{
                removeLoading();
            })
    })
}

function change_email(){
    $('#change_email').modal('show');
    $('#submit_modified_email').off('click');
    $(('#submit_modified_email')).click(function(){
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
        axios.defaults.xsrfCookieName = "csrftoken"
        dispLoading('Loading...');
        axios
            .post('/general-settings/',{
                'post_data_type': 'modified_email',
                'modified_email': $('#modified_email').val()
            })
            .then((res)=>{
                if(res.data.res_code == 0){
                    $('#change_email').modal('hide');
                    general_settings();
                    $('#successful_modification_modal').modal('show');
                }else{
                    alert('error')
                }
            })
            .catch((res)=>{
                console.log('error'+res);
            })
            .finally(()=>{
                removeLoading();
            })
    })
}

function change_deadline(){
    $('#change_deadline').modal('show');
    $('#submit_modified_deadline').off('click');
    $('#submit_modified_deadline').click(function() {
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = "csrftoken";
        dispLoading('Loading...');
        axios
            .post('/general-settings/',{
                'post_data_type': 'modified_deadline',
                'modified_deadline': Number($('#modified_deadline').val())
            })
            .then((res)=>{
                if(res.data.res_code == 0){
                    $('#change_deadline').modal('hide');
                    general_settings();
                    $('#successful_modification_modal').modal('show');
                }else{
                    alert('error')
                }
            })
            .catch((res)=>{
                alert('error');
                console.log(res);
            })
            .finally(()=>{
                removeLoading();
            })
    })
    
}