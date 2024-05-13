<template>
    <div class="container">
        <div class="search-bar-container">
            <input type="text" placeholder="搜索文件名或CID" class="search-bar" />
            <button class="search-button">搜索</button>

            <div style="width: 40px;"></div>

            <div class="create">
                <button @click="dialogFormVisible = true" class="create-button"><span style="color: #69c4cd;">+</span> 加入群组</button>
            </div>

            <el-dialog v-model="dialogFormVisible" title="申请信息" width="500">
                <el-form :model="form">
                    <el-form-item label="群组代号" :label-width="formLabelWidth">
                        <el-input v-model="form.groupId" autocomplete="off" />
                    </el-form-item>
                </el-form>
                <template #footer>
                    <div class="dialog-footer">
                        <el-button @click="dialogFormVisible = false">取消</el-button>
                        <el-button type="primary" @click="joinGroup()">
                            确定
                        </el-button>
                    </div>
                </template>
            </el-dialog>
        </div>

        <h1 class="no-group" v-if="memberGroup.length === 0">您还没有加入群组，点击右上角 <b>加入</b> 🤗</h1>

        <div v-else>
            <div class="groups" v-for="group in memberGroup" :key="group.info">
                <div class="group-item" @click="toggleFiles(group.info.id)">
                    <div style="display: flex; align-items: center;">
                        <div class="status"></div>
                    </div>
                    <div class="group">
                        <div style="font-size: large; font-weight: bold">{{ group.info.name }}</div>
                        <div style="font-size: medium; color: #1d74f2;">{{ group.info.id }}</div>
                    </div>
                    <div class="description" v-if="group.info.description.length != 0">{{ group.info.description }}
                    </div>
                    <div class="description" v-else>无介绍</div>
                    <div class="buttons">
                        <el-button type="primary" plain class="upload-button" @click.stop="downloadAll(group.info.id)">
                            <el-icon color="#409efc">
                                <Download style="width: 20px;" />
                            </el-icon> 全部下载
                        </el-button>
                        <el-button type="danger" plain class="disband-button" @click.stop="quitGroup(group.info.id)">
                            <el-icon color="#f56c6c">
                                <CircleCloseFilled style="width: 20px;" />
                            </el-icon> 退出群组
                        </el-button>
                    </div>
                </div>

                <div class="files" v-if="expandedGroups.includes(group.info.id)">
                    <div class="no-file" v-if="group.files.length === 0">
                        该群组现在还没有任何文件，请联系群主上传🤗
                    </div>

                    <div v-else class="have-file">
                        <el-table :data="group.files" style="width: 100%;" @selection-change="handleSelectionChange">
                            <el-table-column type="selection" width="30" />
                            <el-table-column label="文件名" prop="0" width="150" />
                            <el-table-column label="时间" prop="1" width="100" />
                            <el-table-column label="哈希CID" prop="2" width="420" />
                            <el-table-column label="大小Mb" prop="3" />
                            <el-table-column label="操作">
                                <template #default="{ row }">
                                    <el-button @click="download(row[0], row[2])" type="info" plain
                                        style="width: 80%;">下载</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <div style="margin-top: 10px;">
                            <el-button type="primary" plain @click="toggleSelection(group.files)">
                                下载所选文件
                            </el-button>
                            <el-button type="primary" plain @click="toggleSelection()">
                                清除选择
                            </el-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <el-dialog v-model="toBeConfirmedVisible" title="待确认的请求" width="800">
            <el-table :data="toBeConfirmed">
                <el-table-column type="index"/>
                <el-table-column label="群主ID" prop="owner_id" />
                <el-table-column label="群组ID" prop="group_id" />
                <el-table-column label="状态" prop="status" />
                <el-table-column label="操作">
                    <template #default="{ row }">
                        <div>
                            <el-button @click="confirm(row.owner_id, row.group_id)" type="info" plain>确认</el-button>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="success" @click="confirmAll()" plain>一键确认</el-button>
                    <el-button type="info" @click="toBeConfirmedVisible = false" plain>稍后处理</el-button>
                </div>
            </template>
        </el-dialog>

    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            memberGroup: [
                {
                    "info": {
                        "id": "987654321",
                        "name": "热门动作电影",
                        "description": "用来存放一些电影",
                    },
                    "files": [
                        ["金蝉脱壳.mp4", "2024-05-12", "QmU5EYHCZ5YuKfS6vuHkNZxMC9Up3RNbb8r3ypXJ8AsBzz", "2560"],
                        ["中南海保镖.zip", "2024-05-12", "QmU5EYHCZ5YuKfS6vuHkNZxMC9Up3RNbb8r3ypXJ8AsBzz", "1945.6"]
                    ]
                },
            ],
            dialogFormVisible: false,
            toBeConfirmedVisible: false,
            toBeConfirmed: [],
            form: {
                groupId: '',
            },
            expandedGroups: [],
        };
    },
    methods: {
        async sendUserId() {
            const response = await axios.post('http://localhost:5000/request_group_files', {
                userId: this.$route.params.userId
            });
            if (response.status === 200) {
                // this.memberGroup = response.data.groups;
                console.log(response.data.files)
            } else {
                alert("请求失败，请联系开发人员");
            }
        },
        async getToBeConfirmed() {
            const response = await axios.post('http://localhost:5000/get_approved_requests', {
                requester_id: this.$route.params.userId
            });
            if (response.status === 200) {
                console.log(response.data.requests)
                if (response.data.requests.length == 0) {
                    return;
                }
                this.toBeConfirmed = response.data.requests;
            } else {
                alert("请求失败，请联系开发人员");
            }
            this.toBeConfirmedVisible = true;
        },
        async confirm(ownerId, groupId) {
            const response = await axios.post('http://localhost:5000/process_approved_request', {
                user_id: this.$route.params.userId,
                owner_id: ownerId,
                group_id: groupId,
            });
            if (response.status === 200) {
                console.log(response.data.requests)
                if (response.data.requests.length == 0) {
                    return;
                }
            } else {
                alert("请求失败，请联系开发人员");
            }

            // 找到要移除的数据的索引
            const index = this.toBeConfirmed.findIndex(item => item.owner_id === ownerId && item.group_id === groupId);
            
            if (index !== -1) {
                // 如果找到了匹配的数据，则移除
                this.toBeConfirmed.splice(index, 1);
                console.log(`已成功移除待确认请求`);
            } else {
                alert("未成功移除");
            }
        },
        confirmAll() {
            this.toBeConfirmed.forEach(item => {
                this.confirm(item.ownerId, item.groupId);
            })
            this.toBeConfirmedVisible = true;
        },
        async joinGroup() {
            try {
                const response = await axios.post('http://localhost:5000/request_access', {
                        group_id: this.form.groupId,
                        user_id: this.$route.params.userId,
                        current_time: this.getCurrentTime(),
                    })                
                    if (response.status === 200) {
                        alert("已申请");
                    } else {
                        alert("申请失败");
                    }
                } catch (error) {
                    console.log(error);
                    alert("出现错误，联系开发人员");
            }
            this.dialogFormVisible = false;
        },
        downloadAll(groupId) {
            console.log(`下载了群组 ${groupId} 所有文件`);
        },
        quitGroup(groupId) {
            console.log(`退出群组 ${groupId}`);
        },
        toggleFiles(groupId) {
            if (this.expandedGroups.includes(groupId)) {
                this.expandedGroups = this.expandedGroups.filter(id => id !== groupId);
            } else {
                this.expandedGroups.push(groupId);
            }
        },
        toggleSelection(files) {
            if (files) {
                files.forEach((file) => {
                    this.remove(file[0], file[2]);
                });
                this.$refs.multipleTableRef.clearSelection();
            } else {
                this.$refs.multipleTableRef.clearSelection();
            }
        },
        handleSelectionChange(val) {
            this.multipleSelection = val
        },
        download(fileName, fileHash) {
            console.log(`下载了${fileName}-${fileHash}`);
        },
        getCurrentTime() {
            const currentDate = new Date();

            const year = currentDate.getFullYear();
            const month = currentDate.getMonth() + 1; // 月份是从 0 开始的，所以要加 1
            const day = currentDate.getDate();
            const hours = currentDate.getHours();
            const minutes = currentDate.getMinutes();
            const seconds = currentDate.getSeconds();

            const formattedDate = `${year}/${month}/${day}`;
            const formattedTime = `${hours}:${minutes}:${seconds}`;
            const formattedDateTime = `${formattedDate}-${formattedTime}`;

            return formattedDateTime;
        }
    },
    mounted() {
        console.log("start send!");
        this.sendUserId();
        this.getToBeConfirmed();
    }
}
</script>

<style scoped>
.search-bar-container {
    display: flex;
    justify-content: space-evenly;
    padding: 30px 20px;
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

.no-group {
    padding-top: 20%;
}

.no-file {
    width: 80%;
    height: 40px;
    margin-left: 10%;
    padding-top: 10px;
}

.have-file {
    padding-bottom: 10px;
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
    width: 90%;
    margin-left: 5%;
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