<template>
    <div class="container">
        <div class="search-bar-container">
            <input type="text" placeholder="搜索群组" class="search-bar" />
            <button class="search-button">搜索</button>

            <div style="width: 40px;"></div>

            <div class="create">
                <div style="display: flex; flex-direction: column; margin-right: 20px;">
                    <span style="font-size: larger; font-weight: bold;">{{ ownerGroup.length }}</span><span style="font-size: small;">总群数</span>
                </div>
                <div style="display: flex; flex-direction: column; margin-right: 20px;">
                    <span style="font-size: larger; font-weight: bold;">{{ totalFilesCount }}</span><span style="font-size: small;">总文件数</span>
                </div>
                <div style="display: flex; flex-direction: column; margin-right: 20px;">
                    <span style="font-size: larger; font-weight: bold;">{{ totalFileSize }}</span><span style="font-size: small;">总文件大小</span>
                </div>
                <button class="create-button" @click="dialogFormVisible = true"><span style="color: #69c4cd;">+</span> 创建群组</button>

                <el-dialog v-model="dialogFormVisible" title="Shipping address" width="500">
                    <el-form :model="form">
                        <el-form-item label="Promotion name" :label-width="formLabelWidth">
                            <el-input v-model="form.name" autocomplete="off" />
                        </el-form-item>
                        <el-form-item label="Zones" :label-width="formLabelWidth">
                            <el-select v-model="form.region" placeholder="Please select a zone">
                            <el-option label="Zone No.1" value="shanghai" />
                            <el-option label="Zone No.2" value="beijing" />
                            </el-select>
                        </el-form-item>
                    </el-form>
                    <template #footer>
                        <div class="dialog-footer">
                            <el-button @click="dialogFormVisible = false">Cancel</el-button>
                            <el-button type="primary" @click="createGroup()">
                                Confirm
                            </el-button>
                        </div>
                    </template>
                </el-dialog>

            </div>
        </div>

        <div class="requests-box">
            <div class="requests">
                <el-table
                    :data="requests"
                    style="width: 100%;"
                    >
                    <el-table-column type="index" width="30" />
                    <el-table-column label="申请者" prop="requester_id"/>
                    <el-table-column label="群组ID" prop="group_id"/>
                    <el-table-column label="申请时间" prop="time"/>
                    <el-table-column label="操作">
                        <template #default="{ row }">
                            <div>
                                <el-button @click="permit(row[0], row[2], true)" type="info" plain style="width: 40%;">同意</el-button>
                                <el-button @click="permit(row[0], row[2], false)" type="info" plain style="width: 40%;">拒绝</el-button>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="handleAll">
                <button class="handleall-button" @click="handleAll(true)">全部同意</button>
                <button class="handleall-button" @click="handleAll(false)">全部拒接</button>
            </div>
            <div>
                <div class="refresh-button" @click="refresh()">刷新<br><span style="font-size: 25px;">🆕</span></div>
            </div>
        </div>

        <h1 class="no-group" v-if="ownerGroup.length === 0">您还没有创建群组，点击右上角 <b>创建</b> 🤗</h1>

        <div v-else>
            <div class="groups" v-for="group in ownerGroup" :key="group.info">
                <div class="group-item" @click="toggleGroups(group.info.id)">
                    <div style="display: flex; align-items: center;">
                        <div class="status"></div>
                    </div>
                    <div class="group">
                        <div style="font-size: large; font-weight: bold">{{ group.info.name }}</div>
                        <div style="font-size: medium; color: #1d74f2;">{{ group.info.id }}</div>
                    </div>
                    <div class="description" v-if="group.info.description.length != 0">{{ group.info.description }}</div>
                    <div class="description" v-else>无介绍</div>
                    <div class="buttons">
                        <el-button type="primary" plain class="upload-button" @click.stop="upload()">
                            <el-icon color="#409efc"><UploadFilled style="width: 20px;"/></el-icon> 上传文件
                        </el-button>
                        <el-button type="danger" plain class="disband-button" @click.stop="disband()">
                            <el-icon color="#f56c6c"><RemoveFilled style="width: 20px;"/></el-icon> 解散群组
                        </el-button>
                    </div>
                </div>

                <div class="files" v-if="expandedGroups.includes(group.info.id)">                    
                    <div class="no-file" v-if="group.files.length === 0">
                        <span style="font-size: large;">现在还没有任何文件！使用上方的 <b>上传</b> 按钮为您的群组 节点添加文件。</span> 
                    </div>
                    <div v-else class="have-file">
                        <el-table 
                            :data="group.files"
                            style="width: 100%;"
                            @selection-change="handleSelectionChange"
                            >
                            <el-table-column type="selection" width="30" />
                            <el-table-column label="文件名" prop="0"  width="150"/>
                            <el-table-column label="时间" prop="1" width="100"/>
                            <el-table-column label="哈希CID" prop="2" width="420" />
                            <el-table-column label="大小Mb" prop="3" />
                            <el-table-column label="操作">
                                <template #default="{ row }">
                                    <el-button @click="remove(row[0], row[2])" type="info" plain style="width: 80%;">移除</el-button>
                                </template>
                            </el-table-column>
                        </el-table>

                        <div style="margin-top: 10px;">
                            <el-button type="primary" plain @click="toggleSelection(group.files)">
                                移除所选文件
                            </el-button>
                            <el-button type="primary" plain @click="toggleSelection()">
                                清除选择
                            </el-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
// import axios from 'axios';
// import { ref, nextTick, onMounted } from 'vue'
import { ref } from 'vue'
import { ElTable, ElButton } from 'element-plus'

export default {
    components: {
        ElTable, ElButton,
    },
    data() {
        return {
            ownerGroup: [
                {
                    "info": {
                        "id": "123456789",
                        "name": "豆瓣top100电影",
                        "description": "用来存放一些电影",
                    },
                    "files": [
                        ["肖申克的救赎.mp4", "2024-05-12", "QmU5EYHCZ5YuKfS6vuHkNZxMC9Up3RNbb8r3ypXJ8AsBzz", "2560", "26"],
                        ["霸王别姬.zip", "2024-05-12", "QmU5EYHCZ5YuKfS6vuHkNZxMC9Up3RNbb8r3ypXJ8AsBzz", "1945.6", "18"]
                    ]
                },
                {
                    "info": {
                        "id": "987654321",
                        "name": "热门动作电影",
                        "description": "用来存放一些电影",
                    },
                    "files": [
                        ["金蝉脱壳.mp4", "2024-05-12", "QmU5EYHCZ5YuKfS6vuHkNZxMC9Up3RNbb8r3ypXJ8AsBzz", "2560", "26"],
                        ["中南海保镖.zip", "2024-05-12", "QmU5EYHCZ5YuKfS6vuHkNZxMC9Up3RNbb8r3ypXJ8AsBzz", "1945.6", "18"]
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
                name: '',
                region: '',
            },
            requests: [
                { 'requester_id': 'kyrieirving', 'group_id': '123456789abcdefg', 'time': '2024/5/12-21:25:30' },
                { 'requester_id': 'lebronjames', 'group_id': '987654321abcdefg', 'time': '2024/5/12-21:30:45' },
                { 'requester_id': 'kevindurant', 'group_id': 'abcdefg123456789', 'time': '2024/5/12-21:35:15' }
            ],
            multipleTableRef: ref(null),
            multipleSelection: ref([]),
        };
    },
    methods: {
        createGroup() {
            console.log("创建了一个群组");
            this.dialogFormVisible = false;
        },
        showRequest() {
            // 向 localhost 发送请求
            // fetch('http://localhost/refresh')
            //     .then(response => response.json())
            //     .then(data => {
            //         this.requests.append(data); // 将服务器返回的数据赋值给 requests 数组
            //     })
            //     .catch(error => {
            //         console.error('Error fetching requests:', error);
            //     });
            console.log("向proxy请求申请")
        },
        permit(userId, groupId, allowed) {
            if (allowed) {
                console.log("同意");
            } else {
                console.log("不同意");
            }
        },
        handleAll(allowed) {
            for (const request of this.requests) {
                this.permit(request[0], request[2], allowed);
            }
        },
        refresh() {
            console.log("刷新");
        },
        toggleGroups(groupId) {
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
        remove(fileName, fileHash) {
            console.log(`移除了${fileName}-${fileHash}`);
        },
        upload() {
            console.log("上传文件");
        },
        disband() {
            console.log("解散群组");
        }
    },
    computed: {
        totalFilesCount() {
            let count = 0;
            for (let group of this.ownerGroup) {
                count += group.files.length;
            }
            return count;
        },
        totalFileSize() {
            let totalSize = 0;
            for (let group of this.ownerGroup) {
                for (let file of group.files) {
                let size = parseFloat(file[3]);
                totalSize += size;
                }
            }
            return (totalSize/1024).toFixed(2) + " GiB";
        }
    },
    // mounted() {
    //     // nextTick(() => {
    //     //     this.multipleTableRef = this.$refs.multipleTableRef;
    //     // });
    //     onMounted(() => {
    //         this.multipleTableRef = this.$refs.multipleTableRef;
    //     });
    // },
    // mounted() {
    //     this.fetchPublishedProjects();
    //     this.fetchRaisedProjects();
    // },
    // methods: {
    //     async fetchPublishedProjects() {
    //         const currentUserId = this.$route.params.userId;
    //         try {
    //             const response = await axios.get(`http://localhost:5000/my_published_projects?id=${currentUserId}`);
    //             this.publishedProjects = response.data.projects;
    //             this.publishedProjects.forEach(project => {
    //                 project.photos = require(`@/assets/projects/${JSON.parse(project.photos)[0]}`)

    //                 // console.log(typeof parseInt(project.current_amount));
    //                 project.current_amount = parseInt(project.current_amount);
    //                 project.target_amount = parseInt(project.target_amount);
    //             })
    //         } catch (error) {
    //             console.error('Error fetching projects:', error);
    //         }
    //     },
    //     async fetchRaisedProjects() {
    //         const currentUserId = this.$route.params.userId;
    //         try {
    //             const response = await axios.get(`http://localhost:5000/my_raised_projects?id=${currentUserId}`);
    //             this.raisedProjects = response.data.projects;
    //             this.raisedProjects.forEach(project => {
    //                 project.photos = require(`@/assets/projects/${JSON.parse(project.photos)[0]}`)

    //                 // console.log(typeof parseInt(project.current_amount));
    //                 project.current_amount = parseInt(project.current_amount);
    //                 project.target_amount = parseInt(project.target_amount);
    //             })
    //         } catch (error) {
    //             console.error('Error fetching projects:', error);
    //         }
    //     },
    //     getRandomColor() {
    //         const colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#6A5ACD', '#FF4500', '#20B2AA'];
    //         const randomIndex = Math.floor(Math.random() * colors.length);
    //         return colors[randomIndex];
    //         // return '#' + Math.floor(Math.random() * 16777215).toString(16);
    //     }
    // }
}
</script>

<style scoped>
.search-bar-container {
    display: flex;
    justify-content: space-evenly;
    padding: 0px 20px;
    padding-top: 30px;
    padding-bottom: 20px;
    background-color: #f0f6fa;
}

.search-bar {
    width: 40%;
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

.handleall-button, .create-button {
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

.handleall-button {
    height: 38px;
    background-color: #81afb4;
    margin-bottom: 10px;
}

.requests-box {
    display: flex;
    justify-content: space-between;
    padding: 0px 20px;
    padding-bottom: 10px;
    background-color: #f0f6fa;
}

.requests {
    width: 80%;
}

.handleAll {
    display: flex;
    flex-direction: column;
}

.refresh-button {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    background-color: #234d64;
    border-radius: 5px;
    height: 85px;
    width: 50px;
    font-size: 15px;
    font-weight: bold;
    color: white;
    cursor: pointer;
}

.no-group {
    padding-top: 20%;
}

.no-file {
    height: 50px;
    padding-top: 20px;
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