<template>
  <div>
    <div>
      <el-button type="primary" round size="medium" @click="dialogFormVisible = true">添加父类</el-button>
      <el-button type="primary" round size="medium" @click="subVisible = true">添加子类</el-button>
    </div>
    <el-divider>父类</el-divider>
    <el-table
      :data="tableData1"
      height="300"
      border
      style="width: 100%">
      <el-table-column
        prop="code"
        label="编号"
        width="180">
      </el-table-column>
      <el-table-column
        prop="name"
        label="名字"
        width="180">
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述">
      </el-table-column>
      <el-table-column
        label="操作">
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-edit" circle></el-button>
          <el-button type="danger" icon="el-icon-delete" circle></el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-divider>子类</el-divider>
    <el-table
      :data="tableData2"
      height="600"
      style="width: 100%">
      <el-table-column
        prop="superclass"
        label="父类"
        width="180">
      </el-table-column>
      <el-table-column
        prop="code"
        label="编号"
        width="180">
      </el-table-column>
      <el-table-column
        prop="name"
        label="名字"
        width="180">
      </el-table-column>
      <el-table-column
        prop="example"
        label="例子">
      </el-table-column>
      <el-table-column
        label="操作">
        <template slot-scope="scope">
        <el-button type="primary" icon="el-icon-edit" circle></el-button>
        <el-button type="danger" icon="el-icon-delete" circle></el-button>
      </template>
      </el-table-column>
    </el-table>
    <el-dialog title="添加父类" :visible.sync="dialogFormVisible">
      <el-form ref="superForm" :model="superClass" label-width="80px" :rules="rules">
        <el-form-item label="编码" prop="code">
          <el-input v-model="superClass.code" placeholder="必须是两位"></el-input>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="superClass.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="superClass.description"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="addEditSuperClass">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Kind',
  data () {
    return {
      tableData1: [],
      tableData2: [],
      dialogFormVisible: false,
      subVisible: false,
      superClass: {
        code: '',
        name: '',
        description: ''
      },
      subClass: {
        superclass: '',
        code: '',
        name: '',
        example: ''
      },
      rules: {
        code: [
          {required: true, message: '请输入编码', trigger: 'blur'},
          {min: 2, max: 2, message: '长度是2个字符', trigger: 'blur'}
        ],
        name: [
          {required: true, message: '请输入名称', trigger: 'blur'},
          {min: 1, max: 32, message: '长度在 1 到 32 个字符', trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    getSuperClass () {
      this.$djangoAPI.get('/manage/superclass/').then(res => {
        this.tableData1 = res.results
      })
    },
    getSubClass () {
      // subclass
      this.$djangoAPI.get('/manage/subclass/').then(res => {
        this.tableData2 = res.results
      })
    },
    addEditSuperClass () {
      this.$refs['superForm'].validate((valid) => {
        if (valid) {
          let formData = new FormData()
          formData.append('code', this.superClass.code)
          formData.append('name', this.superClass.name)
          if (this.superClass.describe) {
            formData.append('describe', this.superClass.describe)
          }
          this.$djangoAPI.post('/manage/superclass/', formData).then(res => {
            this.dialogFormVisible = false
            this.getSuperClass()
          })
        }
      })
    }
  },
  created: function () {
    this.getSuperClass()
    this.getSubClass()
  }
}
</script>

<style scoped>

</style>
