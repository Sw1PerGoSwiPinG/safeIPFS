import Dexie from 'dexie';

const db = new Dexie('myDB');

// 定义表格结构
db.version(1).stores({
    KeyTable: '++group_id, file_key, public_key, private_key'
});

// 插入数据到KeyTable
export async function AddKeyToTable(group_id, file_key, public_key, private_key) {
    try {
        await db.KeyTable.add({ group_id, file_key, public_key, private_key });
        console.log('Data added successfully.');
    } catch (error) {
        console.error('Error adding data: ', error);
    }
}

// 查询KeyTable
export async function SearchFromKeyTable(group_id) {
    try {
        const result = await db.KeyTable.where('group_id').equals(group_id).toArray();
        console.log('Search result: ', result);
        return result;
    } catch (error) {
        console.error('Error searching data: ', error);
        return [];
    }
}

// 从KeyTable中删除数据
export async function DeleteFromKeyTable(group_id) {
    try {
        await db.KeyTable.where('group_id').equals(group_id).delete();
        console.log('Data deleted successfully.');
    } catch (error) {
        console.error('Error deleting data: ', error);
    }
}

export default {
    AddKeyToTable,
    SearchFromKeyTable,
    DeleteFromKeyTable
};
