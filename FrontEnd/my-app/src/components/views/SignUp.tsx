import { useState, useEffect } from 'react'
import { useNavigate } from "react-router-dom";

const SignUp = ({ setIsAuth }: { setIsAuth: any }) => {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [pass, setPass] = useState('');
    const [checkEmail, setCheckEmail] = useState(false);
    const [checkPass, setCheckPass] = useState(false);
    const [checkRePass, setCheckRePass] = useState(false);
    const [inputError, setInputError] = useState(false);

    const URL = 'http://127.0.0.1:5000';

    const inputEmail = (event: any) => {
        if (email != null) {
            setEmail(event.target.value);
            setCheckEmail(true);
        }
        else { setCheckEmail(false); }
    }

    const inputPass = (event: any) => {
        if (pass != null) {
            setPass(event.target.value);
            setCheckPass(true);
        }
        else { setCheckPass(false); }
    }

    const inputRePass = (event: any) => {
        if (event.target.value != pass) {
            return setCheckRePass(true);
        }
        return setCheckRePass(false);
    }

    const pushRegister = async () => {
        if (inputError) {
            return
        }
        const response = await fetch(URL, {
            mode: 'cors',
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mail: email, pass: pass }), // フロントエンドから送信するデータ
        })
        const json = await response.json(); // バックエンドから受信したデータ
        setIsAuth[json['isRegister']];
        console.log(json['isRegister']);

    }

    return (
        <div>
            <p>新規登録</p>
            <div className="mail-login">
                <input onChange={inputEmail} placeholder="メールアドレス" />
                {checkEmail ? <p>メールアドレスが不十分です</p> : ""}
                <input onChange={inputPass} placeholder="パスワード" />
                {checkPass ? <p>パスワードが不十分です</p> : ""}
                <input onChange={inputRePass} placeholder="パスワードの確認" />
                {checkRePass ? <p>パスワードが異なっています</p> : ""}
                <button className="login-button" onClick={pushRegister}>新規登録</button>
                {inputError ? <p>全て入力してください</p> : ""}
            </div>
        </div>
    );
}
export default SignUp