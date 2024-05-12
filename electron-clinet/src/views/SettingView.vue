<template>
    <div class="container">
        <!-- 个人信息 -->
        <div class="user-profile">
            <img class="avatar" :src="user.avatarUrl" alt="用户头像" />
            <div class="user-details">
                <h1 class="user-name">{{ $route.params.userId }}</h1>
                <div class="user-email"><b>📫 您的注册邮箱为 </b>{{ user.email }}</div>
                <div class="user-id">🥳 感谢您成为SafeIPFS的 <b>第 1,267,315 位</b> 用户</div>
                <div class="user-tips">📅 下面是您的 <b>密钥信息</b> 您可以查看或删除 </div>
            </div>
        </div>
        <div class="search-bar-container">
            <input type="text" placeholder="搜索文件名或CID" class="search-bar" />
            <button class="search-button">搜索</button>

            <div style="width: 40px;"></div>

            <div class="create">
                <button class="create-button" @click="dialogFormVisible = true">修改个人信息</button>
            </div>
``
            <el-dialog v-model="dialogFormVisible" title="修改信息" width="500">
                    <el-form :model="form">
                        <el-form-item label="原密码" :label-width="formLabelWidth" style="margin-bottom: 50px;">
                            <el-input v-model="form.origin_passwd" autocomplete="off" type="password"/>
                        </el-form-item>
                        <el-form-item label="用户名" :label-width="formLabelWidth">
                            <el-input v-model="form.username" autocomplete="off" />
                        </el-form-item>
                        <el-form-item label="新密码" :label-width="formLabelWidth">
                            <el-input v-model="form.password" autocomplete="off" type="password"/>
                        </el-form-item>
                        <el-form-item label="新邮箱" :label-width="formLabelWidth">
                            <el-input v-model="form.email" autocomplete="off" />
                        </el-form-item>
                    </el-form>
                    <template #footer>
                        <div class="dialog-footer">
                            <el-button @click="dialogFormVisible = false">取消</el-button>
                            <el-button type="primary" @click="changeUserInfo()">
                                确认
                            </el-button>
                        </div>
                    </template>
                </el-dialog>

        </div>

        <div class="warning-box">
            <div class="warning">
                请谨慎修改您的密钥，修改后你在对应群组的身份会失效 (Please change your key carefully).❗
            </div>
        </div>

        <h1 class="no-group" v-if="ownerGroup.length === 0">您还没有相关群组，去 <b>创建</b> 或 <b>加入</b> 吧 🤗</h1>

        <div v-else>
            <div class="groups" v-for="group in ownerGroup" :key="group.info">
                <div class="group-item" @click="toggleFiles(group.info.id)">
                    <div style="display: flex; align-items: center;">
                        <div class="status"></div>
                    </div>
                    <div class="group">
                        <div style="font-size: large; font-weight: bold">{{ group.info.name }}</div>
                        <div style="font-size: medium; color: #1d74f2;">{{ group.info.id }}</div>
                    </div>
                    <div class="buttons">
                        <el-button type="warning" class="upload-button">
                            <el-icon color="#008000" style="margin-right: 10px;">
                                <Connection style="width: 20px;" />
                            </el-icon> 公私钥对
                        </el-button>
                        <el-button type="warning" class="disband-button">
                            <el-icon color="#008000" style="margin-right: 10px;">
                                <Key style="width: 20px;" />
                            </el-icon> AES文件密钥
                        </el-button>
                    </div>
                </div>
            </div>
        </div>

    </div>

</template>

<script>
// import axios from 'axios';

export default {
    data() {
        return {
            user: {
                name: 'Sw1per',
                email: 'zhaojiayi@bupt.edu.cn',
                avatarUrl: ''
            },
            ownerGroup: [
                {
                    "info": {
                        "id": "123456789",
                        "name": "豆瓣top100电影",
                        "description": "用来存放一些电影",
                    },
                    "files": [
                        ["肖申克的救赎.mp4", "bafyreif3tfdpr5n4jdrbielmcapwvbpcthepfkwg2vwonmlhirbjmotedi", "2.5 GiB", "26"],
                        ["霸王别姬.zip", "oiw4elotevbigmcapnfkm2vwihirbjprdbafyrclbwthepedm5nf3tfdjpr", "1.9 GiB", "18"]
                    ]
                },
                {
                    "info": {
                        "id": "987654321",
                        "name": "热门动作电影",
                        "description": "用来存放一些电影",
                    },
                    "files": [
                        ["金蝉脱壳.mp4", "bafyreif3tfdpr5n4jdrbielmcapwvbpcthepfkwg2vwonmlhirbjmotedi", "2.5 GiB", "26"],
                        ["中南海保镖.zip", "oiw4elotevbigmcapnfkm2vwihirbjprdbafyrclbwthepedm5nf3tfdjpr", "1.9 GiB", "18"]
                    ]
                },
                {
                    "info": {
                        "id": "1234abcdefg",
                        "name": "其他电影",
                        "description": "",
                    },
                    "files": []
                }
            ],
            expandedGroups: [],
            dialogFormVisible: false,
            form: {
                origin_passwd: '',
                username: '',
                password: '',
                mail: '',
            },
        };
    },
    methods: {
        toggleFiles(groupId) {
            if (this.expandedGroups.includes(groupId)) {
                this.expandedGroups = this.expandedGroups.filter(id => id !== groupId);
            } else {
                this.expandedGroups.push(groupId);
            }
        },
        getAvatarUrl() {
            const avatar = "default-avatar.jpg"
            this.user.avatarUrl = require(`@/assets/avatars/${avatar}`)
        },
        changeUserInfo() {
            this.dialogFormVisible = false;
        }
    },
    mounted() {
        this.getAvatarUrl();
    }
}
</script>

<style scoped>
.personal-container {
    padding: 20px;
}

.user-profile {
    align-items: center;
    margin-bottom: 20px;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    width: 80%;
    margin-left: auto;
    margin-right: auto;

    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
}

.avatar {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;

    margin-right: 10%;
}

.user-details {
    display: flex;
    flex-direction: column;
    text-align: left;
}

.user-name {
    font-size: 36px;
    font-weight: bold;
}

.user-email, 
.user-tips,
.user-id {
    font-size: 16px;
    color: #666;

    margin-bottom: 10px;
}

.search-bar-container {
    display: flex;
    justify-content: space-evenly;
    padding: 20px 20px;
    background-color: #f0f6fa;
}

.search-bar {
    width: 50%;
    padding-left: 20px;
    border: none;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    font-weight: 600;
}

.search-button {
    padding: 10px 20px;
    border: none;
    background-color: #81afb4;
    color: white;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    font-weight: 700;
}

.search-button:hover {
    transform: scale(1.05);
}

.create {
    display: flex;
}

.create-button {
    padding: 10px 20px;
    margin-left: 10px;
    border: none;
    background-color: #234d64;
    color: white;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    font-weight: 700;
}

.warning-box {
    width: 100%;
    height: 40px;
    display: flex;
}

.warning {
    width: 100%;
    padding-top: 10px;
    font-size: small;
    text-align: center;
    color: #f56c6c;
    background-color: #fef0f0;
    border-top: 2px solid #fab6b6;
    border-bottom: 2px solid #fab6b6;
}

.no-group {
    padding-top: 20%;
}

.no-file {
    width: 80%;
    height: 40px;
    margin-left: 10%;
    padding-top: 10px;
}

.group-item {
    width: 90%;
    margin-left: 5%;
    padding: 30px 0px;
    padding-left: 10px;

    display: flex;
    align-items: center;
    border-bottom: 1px solid grey;
}

.status {
    flex: 1;
    width: 15px;
    height: 15px;

    border-radius: 50%;
    background-color: green;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.group {
    flex: 10;
    margin-left: 5%;
    text-align: left;
    font-size: large;

    background-color: #ffffff;

    display: flex;
    flex-direction: column;
}

.description {
    flex: 10;
    text-align: left;
    display: flex;
    align-items: center;
    color: #7f8491;
}

.buttons {
    flex: 10;
    display: flex;
    align-items: center;
    justify-content: center;
}

.files {
    width: 80%;
    margin-left: 10%;
    background-color: #f0f9fa;
}

.file {
    display: flex;
    min-height: 30px;
    height: auto
}

.file-info {
    min-height: 30px;
    height: auto;
    display: flex;
    align-items: center;
}
</style>