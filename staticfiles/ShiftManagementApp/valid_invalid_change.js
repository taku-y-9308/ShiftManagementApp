/**
 * user_id:number
 * 変更対象のuser_id
 * 
 * target:str
 * 有効と無効を変更するカラム
 * 
 * current_bool:bool
 * 現在のbool値を代入する
 * targetを入力したbool値の反対の値にする
 */
function valid_invalid_change(user_id,target,current_bool){

    //現在アクティブなユーザーを無効化する時に出す警告モーダル
    if(target == 'is_active' && current_bool==true){
        $('#account_disable_warning').modal('show');
    }
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"
    axios
        .post('/valid-invalid-change/',{
            "user_id": user_id,
            "target": target,
            "current_bool": current_bool
        })
        .then((res)=>{
            console.log(res);
            window.globalFunction.account_setting();
        })
        .catch((res)=>{
            console.log(res);
        })
        .finally(()=>{

        })
    
}