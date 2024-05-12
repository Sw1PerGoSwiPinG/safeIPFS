<template>
    <div class="container">
        <div class="main">
            <!-- 整个注册盒子 -->
            <div class="loginbox">
                <!-- 左侧的注册盒子 -->
                <div class="loginbox-in">
                    <!-- 用户头像上传 -->
                    <input type="file" accept="image/*" @change="handleAvatarChange" ref="avatarInput"
                        style="display: none">
                    <div class="avatar-box">
                        <img :src="avatarPreview" class="avatar-preview" alt="点击上传头像" @click="openAvatarInput">
                    </div>
                    <div class="userbox">
                        <span class="iconfont">&#xe817;</span>
                        <input class="user" id="user" v-model="username" placeholder="用户名">
                    </div>
                    <br>
                    <div class="pwdbox">
                        <span class="iconfont">&#xe775;</span>
                        <input class="pwd" id="password" v-model="password" type="password" placeholder="密码">
                    </div>
                    <br>
                    <div class="emailbox">
                        <span class="iconfont">&#xe775;</span>
                        <input class="email" id="email" v-model="email" type="email" placeholder="电子邮箱（可选）">
                    </div>

                    <button type="primary" class="register_btn" @click="login">👈 点击返回登录</button>
                    <div class="log-box" @click="register">注册</div>
                </div>

                <!-- 右侧的注册盒子 -->
                <div class="background"></div>

            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios';

export default {
    name: "RegisterView",
    data: function () {
        return {
            username: '',
            password: '',
            email: 'example@bupt.edn.cn',
            avatarFile: null,
            avatarPreview: 'https://s2.loli.net/2024/04/23/6kLR41dJxe23bXv.jpg' // 用于预览用户头像的图片URL
        }
    },
    methods: {
        openAvatarInput() {
            this.$refs.avatarInput.click();
        },
        handleAvatarChange(event) {
            const file = event.target.files[0];
            if (file) {
                this.avatarFile = file;
                this.avatarPreview = URL.createObjectURL(file);
            }
        },
        login() {
            this.$router.push(`/`);
        },
        async register() {
            try {
                const response = await axios.post('http://localhost:5000/register', {
                    username: this.username,
                    password: this.password,
                });
                console.log(response.data);

                if (response.data.message === "Register successful") {
                    this.$router.push(`${this.username}/home`);
                } else {
                    alert("该用户名已注册，请重新输入");
                    this.avatar = '';
                    this.username = '';
                    this.password = '';
                    this.email = 'example@bupt.edn.cn';
                }
            } catch (error) {
                console.log(error);
                alert("出现错误，联系开发人员");
            }
        }
    }
}
</script>

<style scoped>
img {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    object-fit: cover; 
}

.avatar-box {
    margin-top: 10%;
}

.loginbox {
    display: flex;
    position: absolute;
    width: 100%;
    height: 100%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 #4E655D;
}

.loginbox-in {
    flex: 2;
    background-color:  #34495e ;
}

.userbox, .pwdbox, .emailbox {
    display: flex;
    margin-left: 5%;
    width: 80%;
    padding: 12px 20px;
    border-radius: 50px;
    background-color: rgba(240, 240, 240, 0.2);
}

.userbox {
    margin-top: 5%;
}

.pwdbox, .emailbox {
    margin-top: 2%;
}


.background {
    flex: 3;
    background-image: url('../assets/ipfs.png');
    background-size: cover;
    font-family: sans-serif;
}

.title {
    margin-top: 60%;
    font-weight: bold;
    font-size: 20px;
    color: #ffffff;
}

.title:hover {
    font-size: 21px;
    transition: all 0.4s ease-in-out;
    cursor: pointer;
}

input {
    width: 80%;
    outline-style: none;
    border: 0;
    border-bottom: 1px solid #E9E9E9;
    background-color: transparent;
    font-family: sans-serif;
    font-size: 15px;
    color: #ffffff;
    font-weight: bold;

    border: none;
    outline: none;
}

input:-webkit-autofill {
    /* 修改默认背景框的颜色 */
    box-shadow: 0 0 0px 1000px #89AB9E inset !important;
    /* 修改默认字体的颜色 */
    -webkit-text-fill-color: #445b53;
}

input:-webkit-autofill::first-line {
    /* 修改默认字体的大小 */
    font-size: 15px;
    /* 修改默认字体的样式 */
    font-weight: bold;
}

.log-box {
    width: 80%;
    margin-top: 12%;
    margin-left: 5%;
    padding: 12px 20px;

    color: #ffffff;
    align-items: center;
    text-align: center;
    border-radius: 50px;
    background-color: #3962d6;

    font-size: 16px;
}

.log-box:hover {
    box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19);
    cursor: pointer;
    transition: all 0.2s ease-in;
}

.register_btn {
    background-color: transparent;
    /* Green */
    border: none;
    text-decoration: none;
    font-size: 14px;
    /* border-radius: 20px;   */
    color: #ffffff;
    text-decoration: underline;
    display: flex;
    margin-top: 10%;
    margin-left: 10%;
    outline: none;

}

.register_btn:hover {
    font-weight: bold;
    cursor: pointer;
}

@font-face {
    font-family: "iconfont";
    src: url('../assets/font/iconfont.eot');
    src: url('../assets/font/iconfont.eot?#iefix') format('embedded-opentype'),
        url('../assets/font/iconfont.woff2') format('woff2'), url('../assets/font/iconfont.woff') format('woff'), url('../assets/font/iconfont.ttf') format('truetype'),
        url('../assets/font/iconfont.svg#iconfont') format('svg');
}

.iconfont {
    font-family: "iconfont" !important;
    font-size: 20px;
    font-style: normal;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    height: 22px;
    color: #ffffff;
    margin-right: 10px;
    margin-top: 3px;
}

.icon-key:before {
    content: "\e775";
}

.icon-account:before {
    content: "\e817";
}
</style>