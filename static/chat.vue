<template>
  <div class="root">

    <!-- 左侧 -->
    <div class="left">
      <!-- 会话列表 -->
      <el-button class="new-session" type="info" plain @click="newSession()">新建会话</el-button>
      <el-card class="session-list">
        <div class="session-item" v-for="(session, index) in sessionList" :key="index">
          <div :class="`session-name ${session.session_id == currentSessionId ? 'hight-light' : ''}`" @click="getDialogueHistory(session.session_id)" :contentEditable="session.contentEditable">
          {{ session.session_name }}
          </div>
          <i class="el-icon-edit" v-show="session.isHideButton" @click="changeToSave(session)"></i>
          <i class="el-icon-delete" v-show="session.isHideButton" @click="deleteSession(session.session_id)"></i>
          <i class="el-icon-receiving" v-show="!session.isHideButton" @click="saveChange(session)"></i>
        </div>
      </el-card>
    </div>

    <!-- 右侧 -->
    <div class="right">
      <div class="main">
        <!-- 通知 -->
        <el-alert class="alert" type="info" effect="dark" show-icon title="GPT-3.5-Turbo" description="训练数据来源于2021年9月之前的互联网信息，对于2021年9月之后的事件可能无法提供准确的答案。"></el-alert>
        <!-- 聊天区域 -->
        <div class="chat-area" v-for="(obj, index) in messageList" :key="index">
          <!-- 用户 -->
          <div class="user">
            <div class="question">
              <span v-for="(item, index) in obj.question" :key="index">{{item}}</span>
            </div>
            <div class="user-avatar">
              <el-avatar size="large">You</el-avatar>
            </div>
          </div>
          <!-- AI -->
          <div class="ai">
            <div class="ai-avatar"></div>
            <div class="answers-w">
              <div class="answers">
                <span v-for="(item, index) in obj.answer" :key="index" v-html="item && item.replace(/\n/g, '<br>')"></span>
              </div>
              <el-button class="btn" icon="el-icon-switch-button" @click="stop" type="text" size="small"
               v-if="(animationIntervalId ? true : false) && index == messageList.length - 1">
               停止
              </el-button>
            </div>
          </div>
        </div>
      </div>
      <!-- 输入区域 -->
      <div class="playground">
        <div class="content">
          <el-input class="input-area" type="textarea" autofocus rows="2" v-model="content" @keydown.native="keydown"
            :disabled="animationIntervalId ? true : false" placeholder="请输入问题并发送(Enter)...  (Shift + Enter = 换行)" >
          </el-input>
        </div>
        <el-button class="send" @click="ask(this.currentSessionId)" type="primary" size="small"
         icon="el-icon-s-promotion" :disabled="animationIntervalId ? true : false">
        </el-button>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  data () {
    return {
      content: '',
      output: '',
      animationIntervalId: null,
      messageList: [],
      answers: [],
      loading: false,
      // 当前会话id
      currentSessionId: '',
      // 会话列表
      sessionList: [],
      // 是否禁止编辑
      isNoEdit: true,
      // 是否隐藏按钮
      isHideButton: true
    }
  },
  computed: {
    // 获取存放在localStorage的用户id
    uid () {
      let uid = ''
      if (localStorage.getItem('login')) {
        let login = JSON.parse(localStorage.getItem('login'))
        uid = this.$store.state.login.id
          ? this.$store.state.login.id
          : login.id
            ? login.id
            : ''
      }
      return uid
    }
  },
  watch: {
    // 过滤内容中的undefined
    answers (content) {
      return content.filter((item) => item !== undefined)
    }
  },
  methods: {
    // 切换到保存状态
    changeToSave (obj) {
      obj.isHideButton = !obj.isHideButton
      obj.isNoEdit = !obj.isNoEdit
      obj.contentEditable = !obj.contentEditable
    },
    // 保存改变
    saveChange (obj) {
      this.changeToSave(obj)
      this.renameSession(obj.session_id, obj.session_name)
    },
    // 触发按键事件
    keydown (event) {
      // 如果按下的是enter，则发送
      if (event.keyCode === 13) {
        // ie阻止冒泡行为
        event.cancelBubble = true
        // Firefox阻止冒泡行为
        event.stopPropagation()
        // 阻止默认事件
        event.preventDefault()
        this.ask()
      }
      // 如果按下的是shift+enter，则换行
      if (event.shiftKey && event.keyCode === 13) {
        event.cancelBubble = true
        event.stopPropagation()
        event.preventDefault()
        this.content += '\n'
      }
    },
    // 提问
    ask () {
      if (this.content === '') {
        this.$message.error('内容不能为空')
        return
      }
      if (this.currentSessionId === '') {
        this.newSession()
        this.currentSessionId = this.sessionList[0].session_id
      }
      this.loading = true
      this.messageList.push({
        question: [this.content],
        answer: []
      })
      this.answers = []
      this.eventSource = new EventSource('https://xxx.com/api/chatPlus?content=' + this.content + '&session_id=' + this.currentSessionId, { withCredentials: true })
      console.log(this.currentSessionId)
      this.eventSource.onmessage = (event) => {
        // 如果message的数据为{}，则停止请求这个接口
        if (event.data === '{}') {
          this.content = ''
          this.loading = false
          this.eventSource.close()
        } else {
          let data = this.checkJSON(event.data) ? JSON.parse(event.data) : ''
          let message = data.content
          this.answers.push(message)
        }
      }
      this.showAnswers()
    },
    // 每隔100ms输出一个字符块
    showAnswers () {
      let currentIndex = 0
      let content = []
      let index = this.messageList.length - 1
      clearInterval(this.animationIntervalId)
      this.animationIntervalId = null
      this.animationIntervalId = setInterval(() => {
        if (currentIndex < this.answers.length) {
          content.push(this.answers[currentIndex])
          this.$set(this.messageList[index], 'answer', content)
          currentIndex++
        } else if (!this.loading) {
          clearInterval(this.animationIntervalId)
          this.animationIntervalId = null
        }
      }, 100)
    },
    // 停止
    stop () {
      this.eventSource.close()
      clearInterval(this.animationIntervalId)
      this.animationIntervalId = null
    },
    // 验证数据JSON格式
    checkJSON (data) {
      if (data.split('"').length - 1 === 4) {
        return data
      }
      if (data.split('"').length - 1 < 4) {
        return ''
      }
      if (data.split('"').length - 1 > 4) {
        let splitArr = data.split('"')
        let newString = ''
        for (let key in splitArr) {
          if (splitArr[key].length > 0) {
            newString +=
              newString.length === 0 ? splitArr[key] : `"` + splitArr[key]
          }
        }
        return newString
      }
    },
    // 获取会话列表
    async getSessionList () {
      const res = await this.$axios.get('https://xxx.com/api/getSessionList?uid=' + this.uid)
      if (res.data.code !== 200) {
        this.$message.error('会话列表获取失败')
      }
      if (res.data.data && res.data.data.length && res.data.data.length > 0) {
        res.data.data.map(v => {
          v.isHideButton = true
          v.isNoEdit = true
        })
      }
      this.sessionList = res.data.data
      if (this.sessionList.length === 0 || this.sessionList === null) {
        // 默认选中第一个会话
        this.currentSessionId = this.sessionList[0].session_id
      }
    },
    // 新建会话
    async newSession () {
      let params = {
        uid: this.uid
      }
      await this.$axios.post('https://xxx.com/api/newSession', params).then((res) => {
        if (res.data.code !== 200) {
          this.$message.error('新建会话失败')
        }
        this.getSessionList()
      })
    },
    // 删除会话
    deleteSession (sessionId) {
      let params = {
        session_id: sessionId
      }
      this.$axios.post('https://xxx.com/api/deleteSession', params).then((res) => {
        if (res.data.code !== 200) {
          this.$message.error('删除会话失败')
        }
        this.getSessionList()
        // 清理对话历史
        this.messageList = []
      })
    },
    // 重命名会话名称
    renameSession (sessionId, sessionName) {
      let params = {
        session_id: sessionId,
        session_name: sessionName
      }
      this.$axios.post('https://xxx.com/api/renameSession', params).then((res) => {
        if (res.data.code !== 200) {
          this.$message.error('重命名会话名称失败')
        }
        this.getSessionList()
      })
    },
    // 获取对话历史
    getDialogueHistory (sessionId) {
      this.currentSessionId = sessionId
      let params = {
        session_id: sessionId
      }
      this.$axios.get('https://xxx.com/api/getDialogueHistory', { params }).then((res) => {
        if (res.data.code !== 200) {
          this.$message.error('获取对话历史失败')
        }
        // 将对话历史添加到对话中
        this.messageList = res.data.data
      })
    }
  },
  mounted () {
    this.getSessionList().then(() => {
      this.getDialogueHistory(this.currentSessionId)
    })
  },
  destroyed () {
    clearInterval(this.animationIntervalId)
    this.animationIntervalId = null
  }
}
</script>

<style lang="scss" scoped>
.root {
  width: 1500px;
  font-family: "Microsoft YaHei", Arial, Helvetica, sans-serif;
  display: flex;
}

.new-session {
  margin: 10px 0;
  width: 100%;
  font-weight: bold;
  font-size: 20px;
  font-family: "Microsoft YaHei", Arial, Helvetica, sans-serif;
  background-color: #141415;
  &:hover{
    background: radial-gradient(circle, #409eff, #141415);
  }
}

.session-list {
  width: 260px;
  height: 613px;
  background: radial-gradient(circle, #409eff, #141415);
}

.session-item {
  background-color: #141415;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 10px;
  margin-bottom: 10px;
  padding: 5px;
}

.session-name {
  height: 28px;
  width: 160px;
  color: #fff;
  font-size: 14px;
  margin-left: 5px;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 150px;
  line-height: 28px;
  &:hover {
    color: #409eff;
  }
}
.hight-light{
  color: #409eff;
}

i {
  color: #fff;
  cursor: pointer;
  &:hover {
    color: #409eff;
  }
}

.right {
  margin-top: 10px;
  height: 670px;
  background: url('../../assets/tech.gif') no-repeat;
  background-size: cover;
}

.main {
  height: 490px;
  width: 820px;
  padding: 0 30px 30px;
  max-height: 600px;
  overflow: auto;
  margin-top: 10px;
  border-radius: 5px;

  .input-area {
    margin: 10px 0;
    height: 600px;
    font-family: "Microsoft YaHei", Arial, Helvetica, sans-serif;
  }
}

.chat-area {
  width: 800px;

  .ai {
    display: flex;
    margin-top: 30px;

    .ai-avatar {
      border-radius: 50%;
      width: 40px;
      height: 40px;
      background: url("../assets/ChatGPT.png") no-repeat center;
      background-size: contain;
    }

    .answers-w {
      display: flex;
      flex-flow: column;
      align-items: flex-start;
      max-width: 800px;
      position: relative;

      .answers {
        background: #585858;
        color: #fff;
        max-width: 680px;
        font-family: "Microsoft YaHei", Arial, Helvetica, sans-serif;
        font-size: 14px;
        padding: 10px;
        margin: 0px 10px;
        border-radius: 8px;
        position: relative;

        &:before {
          content: "";
          position: absolute;
          left: -5px;
          top: 3px;
          border-top: 6px solid transparent;
          border-bottom: 6px solid transparent;
          border-right: 6px solid #585858;
          width: 0;
          height: 0;
        }
      }

      .font-length {
        color: #999;
        font-size: 12px;
        position: absolute;
        bottom: -15px;
        right: 10px;
        transform: scale(0.8);
        min-width: 54px;
      }

      .btn {
        position: absolute;
        bottom: -25px;
        left: 20px;
      }
    }
  }

  .user {
    display: flex;
    margin-top: 16px;
    justify-content: flex-end;

    .user-avatar {
      border-radius: 50%;
      width: 40px;
      height: 40px;
    }

    .question {
      background: #409eff;
      color: #fff;
      font-family: "Microsoft YaHei", Arial, Helvetica, sans-serif;
      font-size: 14px;
      padding: 10px;
      margin: 0px 10px;
      border-radius: 8px;
      position: relative;

      &:before {
        content: "";
        position: absolute;
        right: -5px;
        top: 3px;
        border-top: 6px solid transparent;
        border-bottom: 6px solid transparent;
        border-left: 6px solid #409eff;
        width: 0;
        height: 0;
      }
    }
  }
}

.playground {
  bottom: 300px;
  margin: 30px;
}
.content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.alert{
  color: #fff;
  background: radial-gradient(circle, #409eff, #141415);
}
</style>

<style>
.el-textarea__inner {
  font-family: "Microsoft YaHei", Arial, Helvetica, sans-serif !important;
  font-size: 16px;
}
</style>
