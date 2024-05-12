<template>
    <div class="create-container">
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
                <button class="create-button"><span style="color: #69c4cd;">+</span> 创建群组</button>
            </div>
        </div>

        <h1 class="no-group" v-if="ownerGroup.length === 0">您还没有创建群组，点击右上角 <b>创建</b> 🤗</h1>

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
                    <div class="description" v-if="group.info.description.length != 0">{{ group.info.description }}</div>
                    <div class="description" v-else>无介绍</div>
                    <div class="buttons">
                        <el-button type="primary" plain class="upload-button">
                            <el-icon color="#409efc"><UploadFilled style="width: 20px;"/></el-icon> 上传文件
                        </el-button>
                        <el-button type="danger" plain class="disband-button">
                            <el-icon color="#f56c6c"><RemoveFilled style="width: 20px;"/></el-icon> 解散群组
                        </el-button>
                    </div>
                </div>

                <div class="files" v-if="expandedGroups.includes(group.info.id)">
                    <div class="no-file" v-if="group.files.length === 0">
                        现在还没有任何文件！使用上方的 <b>上传</b> 按钮为您的本地IPFS 节点添加文件。
                    </div>

                    <div v-else>
                        <div class="file" v-for="file in group.files" :key="file[1]">
                            <el-icon style="width: 40px; height: 30px;display: flex; align-items: center">
                                <Link style="width: 20px;"/>
                            </el-icon>
                            <div class="file-info">{{ file[0] }} - {{ file[1] }} - {{ file[2] }} - 下载{{ file[3] }}次</div>
                        </div>
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
        };
    },
    methods: {
        toggleFiles(groupId) {
            if (this.expandedGroups.includes(groupId)) {
                this.expandedGroups = this.expandedGroups.filter(id => id !== groupId);
            } else {
                this.expandedGroups.push(groupId);
            }
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
                let size = parseFloat(file[2]);
                totalSize += size;
                }
            }
            return totalSize.toFixed(2) + " GiB";
        }
    }
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
    padding: 30px 20px;
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
    height: 20%;
    margin-left: 10%;
}

/* .groups {
    margin: 20px 0px;
} */

.group-item {
    width: 90%;
    margin-left: 5%;
    padding: 30px 0px;
    padding-left: 10px;

    display: flex;
    align-items: center;
    border-bottom: 2px solid grey;
}

.status {
    flex: 1;
    width: 20px;
    height: 20px;

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
}

/* .upload-button, .disband-button {
    height: 50%;
    width: 100%;
} */

/* .upload-button {
    background-color: #234d64;
}

.disband-button {
    background-color: #f56c6c;
} */

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