<template>
    <div class="container">
        <div class="search-bar-container">
            <input type="text" placeholder="搜索群组" class="search-bar" />
            <button class="search-button">搜索</button>

            <div style="width: 40px;"></div>

            <div class="create">
                <div style="display: flex; flex-direction: column; margin-right: 20px;">
                    <span style="font-size: larger; font-weight: bold;">{{ ownerGroup.length }}</span><span
                        style="font-size: small;">总群数</span>
                </div>
                <div style="display: flex; flex-direction: column; margin-right: 20px;">
                    <span style="font-size: larger; font-weight: bold;">{{ totalFilesCount }}</span><span
                        style="font-size: small;">总文件数</span>
                </div>
                <div style="display: flex; flex-direction: column; margin-right: 20px;">
                    <span style="font-size: larger; font-weight: bold;">{{ totalFileSize }}</span><span
                        style="font-size: small;">总文件大小</span>
                </div>
                <button class="create-button" @click="dialogFormVisible = true"><span style="color: #69c4cd;">+</span>
                    创建群组</button>

                <el-dialog v-model="dialogFormVisible" title="创建群组" width="500">
                    <el-form :model="form">
                        <el-form-item label="群组名称" :label-width="formLabelWidth">
                            <el-input v-model="form.group_name" autocomplete="off" />
                        </el-form-item>
                        <el-form-item label="群组描述" :label-width="formLabelWidth">
                            <!-- <el-select v-model="form.region" placeholder="Please select a zone">
                            <el-option label="Zone No.1" value="shanghai" />
                            <el-option label="Zone No.2" value="beijing" />
                            </el-select> -->
                            <el-input v-model="form.group_description" autocomplete="off" />
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
                <el-table :data="requests" style="width: 100%;">
                    <el-table-column type="index" width="30" />
                    <el-table-column label="申请者" prop="requester_id" />
                    <el-table-column label="群组ID" prop="group_id" />
                    <el-table-column label="申请时间" prop="time" />
                    <el-table-column label="操作">
                        <template #default="{ row }">
                            <div>
                                <el-button @click="permit(row.requester_id, row.group_id, true)" type="info" plain
                                    style="width: 40%;">同意</el-button>
                                <el-button @click="permit(row.requester_id, row.group_id, false)" type="info" plain
                                    style="width: 40%;">拒绝</el-button>
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
                    <div class="description" v-if="group.info.description.length != 0">{{ group.info.description }}
                    </div>
                    <div class="description" v-else>无介绍</div>
                    <div class="buttons">
                        <!-- <input type="file" plain class="upload-button" @change="uploadFile($event, group.info.id)"> -->
                        <el-button type="primary" plain class="show-upload" @click.stop="showUploadDialog()">
                            <el-icon color="#409efc">
                                <UploadFilled style="width: 20px;" />
                            </el-icon> 上传文件
                        </el-button>

                        <el-button type="danger" plain class="disband-button" @click.stop="disbandGroup()">
                            <el-icon color="#f56c6c">
                                <RemoveFilled style="width: 20px;" />
                            </el-icon> 解散群组
                        </el-button>
                    </div>
                </div>

                <div class="files" v-if="expandedGroups.includes(group.info.id)">
                    <div class="no-file" v-if="group.files.length === 0">
                        <span style="font-size: large;">现在还没有任何文件！使用上方的 <b>上传</b> 按钮为您的本地IPFS 节点添加文件。</span>
                    </div>
                    <div v-else class="have-file">
                        <el-table :data="group.files" style="width: 100%;"
                            @selection-change="handleSelectionChange">
                            <el-table-column type="selection" width="30" />
                            <el-table-column label="文件名" prop="0" width="150" />
                            <el-table-column label="时间" prop="1" width="100" />
                            <el-table-column label="哈希CID" prop="2" width="420" />
                            <el-table-column label="大小Mb" prop="3" />
                            <el-table-column label="操作">
                                <template #default="{ row }">
                                    <el-button @click="remove(row[0], row[2])" type="info" plain
                                        style="width: 80%;">移除</el-button>
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

                <el-dialog v-model="uploadVisible" title="" width="400" align-center>
                    <el-upload
                        ref="upload"
                        class="upload-file"
                        action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
                        :limit="1"
                        :on-exceed="handleExceed"
                        :auto-upload="false"
                        @change="handleFileChange"
                    >
                        <template #trigger>
                            <el-button type="primary" plain>选择文件</el-button>
                        </template>
                        <template #tip>
                            <div class="el-upload__tip text-red"></div>
                        </template>
                        <el-button class="ml-3" type="success" plain @click="uploadFile(group.info.id)" style="margin-left: 20px">
                            上传IPFS
                        </el-button>
                    </el-upload>
                </el-dialog>
            </div>
        </div>
    </div>

</template>

<script>
import axios from 'axios';
// import { ref, nextTick, onMounted } from 'vue'
// import { ref } from 'vue'
import { ElTable, ElButton } from 'element-plus'
import CryptoService from '@/services/CryptoService';
import { AddKeyToTable, SearchFromKeyTable } from '@/services/DataBase';
import { create } from 'kubo-rpc-client';

export default {
    components: {
        ElTable, ElButton,
    },
    data() {
        return {
            ipfs: null,
            ownerGroup: [],
            expandedGroups: [],
            dialogFormVisible: false,
            uploadVisible: false,
            file: null,
            form: {
                group_name: '',
                group_description: '',
            },
            requests: [],
        };
    },
    methods: {
        bufferToHex(buffer) {
            const bytes = new Uint8Array(buffer);
            return bytes.reduce((str, byte) => str + byte.toString(16).padStart(2, '0'), ''); // 将每个字节转换为十六进制
        },
        async getKeyAsHexString() {
            const key = await CryptoService.generateAESKey(); // 生成密钥
            // console.log(key);
            const exportedKey = await window.crypto.subtle.exportKey("raw", key); // 导出为ArrayBuffer
            return this.bufferToHex(exportedKey); // 转换为十六进制字符串
        },
        hexToBuffer(hexString) {
            const length = hexString.length / 2;
            const buffer = new Uint8Array(length);
            for (let i = 0; i < length; i++) {
                const index = i * 2;
                const byteValue = parseInt(hexString.substring(index, index + 2), 16);
                buffer[i] = byteValue;
            }
            return buffer.buffer; // 返回ArrayBuffer
        },
        async importKeyFromHex(hexString) {
            const keyBuffer = this.hexToBuffer(hexString);
            const keyAlgorithm = {
                name: "AES-CBC",
                length: 256 // 确保这里的长度和算法与你原始生成密钥时使用的设置匹配
            };
            const key = await window.crypto.subtle.importKey(
                "raw", // 密钥格式
                keyBuffer, // 十六进制字符串转换来的ArrayBuffer
                keyAlgorithm, // 定义密钥的算法
                true, // 是否可导出
                ["encrypt", "decrypt"] // 密钥用途
            );
            return key;
        },
        async createGroup() {
            console.log("创建了一个群组");
            this.dialogFormVisible = false;
            var user_id = this.$route.params.userId;
            var group_name = this.form.group_name;
            var group_description = this.form.group_description;
            // var file_key = await CryptoService.generateAESKey();
            var file_key = await this.getKeyAsHexString();
            // console.log(this.importKeyFromHex(file_key));

            try {
                const response = await axios.post('http://localhost:5000/create_group', {
                    user_id: user_id,
                    group_name: group_name,
                    group_description: group_description,
                    file_key: file_key
                })
                console.log(response.data.group_id);
                try {
                    AddKeyToTable(response.data.group_id, group_name, group_description, file_key, response.data.public_key, response.data.private_key);
                    console.log("成功添加到数据库");
                } catch (error) {
                    console.log(error);
                }
                this.ownerGroup.push({
                    "info": {
                        "id": response.data.group_id,
                        "name": group_name,
                        "description": group_description,
                    },
                    "files": []
                });
            } catch (error) {
                console.log(error);
            }

        },
        async permit(userId, groupId, allowed) {
            if (allowed) {
                try {
                    const response = await axios.post('http://localhost:5000/get_public_key', {
                        owner_id: this.$route.params.userId,
                        requester_id: userId,
                        group_id: groupId,
                    })
                    if (response.status === 200) {
                        alert("已同意");
                    } else {
                        alert("同意失败");
                    }
                } catch (error) {
                    console.log(error);
                    alert("出现错误，联系开发人员");
                }
            } else {
                alert("已拒绝");
            }

            console.log(userId)
            console.log(groupId)
            // 找到要移除的数据的索引
            const index = this.requests.findIndex(request => request.requester_id === userId && request.group_id === groupId);
            
            if (index !== -1) {
                // 如果找到了匹配的数据，则移除
                this.requests.splice(index, 1);
                console.log(`已成功移除请求：requester_id=${userId}, group_id=${groupId}`);
            } else {
                alert("未成功移除");
            }
        },
        handleAll(allowed) {
            this.requests.forEach(request => {
                this.permit(request.userId, request.groupId, allowed);
            })
        },
        async refresh() {
            try {
                const response = await axios.post('http://localhost:5000/get_requests', {
                    user_id: this.$route.params.userId,
                })
                console.log(response.data.requests);
                this.requests = response.data.requests;
            } catch (error) {
                console.log(error);
                alert("出现错误，联系开发人员");
            }
        },
        async getMyGroupAndFiles() {
            // try {
            //     const response = await axios.post('http://localhost:5000/get_requests', {
            //         user_id: this.$route.params.userId,
            //     })
            //     console.log(response.data.requests);
            //     this.ownerGroup = response.data.requests;
            // } catch (error) {
            //     console.log(error);
            //     alert("出现错误，联系开发人员");
            // }
            console.log("获取我创建的群组");
        },
        disbandGroup(groupId) {
            console.log(`解散 ${groupId} 号群组`);
        },
        showUploadDialog() {
            this.uploadVisible = true;
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
        async remove(fileName, fileHash) {
            try {
                await this.ipfs.pin.rm(fileHash);
                console.log('File with CID:', fileHash, 'removed successfully');
                console.log(`移除了${fileName}-${fileHash}`);
                // TODO: 向后端发出删除数据库请求
                this.ownerGroup.forEach(group => {
                    group.files = group.files.filter(file => file[0] !== fileName);
                });
            } catch (error) {
                console.error('Error removing the file:', error);
            }
        },
        handleFileChange(file) {
            this.file = file.raw;
            console.log(this.file);
        },
        // async uploadFile(event, groupId) {                        
        async uploadFile(groupId) {                        
            // const file = event.target.files[0];
            const file = this.file;
            if (!file) {
                return;
            }

            const result = await SearchFromKeyTable(groupId);
            // const result = results[0].file_key;
            console.log(result.file_key);
            var file_key = await this.importKeyFromHex(result.file_key);

            const reader = new FileReader();

            // 将文件读取为Blob对象
            reader.onload = async () => {
                const blob = new Blob([reader.result], { type: file.type });

                console.log('file_key:', file_key); // Ensure the key is logged after it's generated

                const encryptedBlob = await CryptoService.encryptFile(blob, file_key);

                this.progress = 0; // Reset progress for new upload
                try {
                    const fileAdded = await this.ipfs.add(encryptedBlob, {
                        progress: (bytes) => {
                            this.progress = (bytes / blob.size) * 100;
                        }
                    });

                    // 获取cid
                    const ipfs_hash = fileAdded.cid;
                    console.log('File uploaded with CID:', ipfs_hash.toString());
                    // 获取文件名
                    const file_name = file.name;
                    console.log('File name:', file_name);

                    try {
                        const response = await axios.post('http://localhost:5000/upload_file', {
                            group_id: groupId,
                            file_name: file_name,
                            ipfs_hash: ipfs_hash.toString(),
                            file_size: blob.size,
                            upload_date: new Date().toLocaleDateString(),
                        })
                        console.log(response.data.message);
                        this.ownerGroup.forEach(group => {
                            if (group.info.id === groupId) {
                                group.files.push([file_name, new Date().toLocaleDateString(), ipfs_hash.toString(), (blob.size / (1024 * 1024)).toFixed(2)]);
                            }
                        });
                    } catch (error) {
                        console.error('Error uploading the file:', error);
                    }
                } catch (error) {
                    console.error('Error uploading the file:', error);
                }
            };

            reader.readAsArrayBuffer(file); // 读取文件内容
        },
        disband() {
            console.log("解散群组");
        },
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
            return (totalSize / 1024).toFixed(2) + " GiB";
        }
    },
    mounted() {
        // this.refresh();
        this.getMyGroupAndFiles();
        this.ipfs = create("http://localhost:5001/api/v0");
    }
    // mounted() {
    //     // nextTick(() => {
    //     //     this.multipleTableRef = this.$refs.multipleTableRef;
    //     // });
    //     onMounted(() => {
    //         this.multipleTableRef = this.$refs.multipleTableRef;
    //     });
    // },
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

.handleall-button,
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

.uploadDialog {
    display: flex;
    flex-direction: column;
}

/* .upload-button {
    width: 20%;
    height: 10%;
} */

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