<template>
  <div class="auth-container">
    <dv-border-box-8 :dur="5">
      <div class="auth-content">
        <!-- 登录表单 -->
        <div v-if="currentView === 'login'" class="login-form">
          <h2>医疗数据分析系统</h2>
          <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef">
            <el-form-item prop="username">
              <el-input 
                v-model="loginForm.username" 
                placeholder="用户名"
                prefix-icon="el-icon-user"
                size="large"
              ></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input 
                v-model="loginForm.password" 
                type="password" 
                placeholder="密码"
                prefix-icon="el-icon-lock"
                size="large"
                @keyup.enter="handleLogin"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button 
                type="primary" 
                size="large" 
                style="width: 100%"
                :loading="loading"
                @click="handleLogin"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>
          <div class="auth-links">
            <el-button type="text" @click="switchToRegister">注册账号</el-button>
            <el-button type="text" @click="switchToReset">忘记密码</el-button>
          </div>
        </div>

        <!-- 注册表单 -->
        <div v-else-if="currentView === 'register'" class="register-form">
          <h2>用户注册</h2>
          <el-form :model="registerForm" :rules="registerRules" ref="registerFormRef">
            <el-form-item prop="username">
              <el-input 
                v-model="registerForm.username" 
                placeholder="用户名"
                prefix-icon="el-icon-user"
              ></el-input>
            </el-form-item>
            <el-form-item prop="email">
              <el-input 
                v-model="registerForm.email" 
                placeholder="邮箱"
                prefix-icon="el-icon-message"
              ></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input 
                v-model="registerForm.password" 
                type="password" 
                placeholder="密码"
                prefix-icon="el-icon-lock"
              ></el-input>
            </el-form-item>
            <el-form-item prop="confirmPassword">
              <el-input 
                v-model="registerForm.confirmPassword" 
                type="password" 
                placeholder="确认密码"
                prefix-icon="el-icon-lock"
              ></el-input>
            </el-form-item>
            <el-form-item prop="role">
              <el-select v-model="registerForm.role" placeholder="选择角色" style="width: 100%">
                <el-option label="医生" value="doctor"></el-option>
                <el-option label="护士" value="nurse"></el-option>
                <el-option label="管理员" value="admin"></el-option>
                <el-option label="研究员" value="researcher"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button 
                type="primary" 
                size="large" 
                style="width: 100%"
                :loading="loading"
                @click="handleRegister"
              >
                注册
              </el-button>
            </el-form-item>
          </el-form>
          <div class="auth-links">
            <el-button type="text" @click="switchToLogin">返回登录</el-button>
          </div>
        </div>

        <!-- 密码重置表单 -->
        <div v-else-if="currentView === 'reset'" class="reset-form">
          <h2>重置密码</h2>
          <el-form :model="resetForm" :rules="resetRules" ref="resetFormRef">
            <el-form-item prop="email">
              <el-input 
                v-model="resetForm.email" 
                placeholder="注册邮箱"
                prefix-icon="el-icon-message"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button 
                type="primary" 
                size="large" 
                style="width: 100%"
                :loading="loading"
                @click="handleReset"
              >
                发送重置邮件
              </el-button>
            </el-form-item>
          </el-form>
          <div class="auth-links">
            <el-button type="text" @click="switchToLogin">返回登录</el-button>
          </div>
        </div>
      </div>
    </dv-border-box-8>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Auth',
  data() {
    // 密码确认验证
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }

    return {
      currentView: 'login', // login, register, reset
      loading: false,
      
      // 登录表单
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },

      // 注册表单
      registerForm: {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        role: ''
      },
      registerRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度在3-20个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 20, message: '密码长度在6-20个字符', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ],
        role: [
          { required: true, message: '请选择角色', trigger: 'change' }
        ]
      },

      // 重置表单
      resetForm: {
        email: ''
      },
      resetRules: {
        email: [
          { required: true, message: '请输入注册邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 切换视图
    switchToLogin() {
      this.currentView = 'login'
      this.resetForms()
    },
    switchToRegister() {
      this.currentView = 'register'
      this.resetForms()
    },
    switchToReset() {
      this.currentView = 'reset'
      this.resetForms()
    },

    // 重置表单
    resetForms() {
      this.$nextTick(() => {
        if (this.$refs.loginFormRef) this.$refs.loginFormRef.resetFields()
        if (this.$refs.registerFormRef) this.$refs.registerFormRef.resetFields()
        if (this.$refs.resetFormRef) this.$refs.resetFormRef.resetFields()
      })
    },

    // 处理登录
    async handleLogin() {
      try {
        await this.$refs.loginFormRef.validate()
        this.loading = true

        const response = await axios.post('/api/user/login', {
          username: this.loginForm.username,
          password: this.loginForm.password
        })

        if (response.data.code === 200) {
          this.$message.success('登录成功')
          // 存储用户信息和token
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('user', JSON.stringify(response.data.user))
          
          // 跳转到首页
          this.$router.push('/')
        } else {
          this.$message.error(response.data.message || '登录失败')
        }
      } catch (error) {
        console.error('登录错误:', error)
        this.$message.error('登录失败，请检查网络连接')
      } finally {
        this.loading = false
      }
    },

    // 处理注册
    async handleRegister() {
      try {
        await this.$refs.registerFormRef.validate()
        this.loading = true

        const response = await axios.post('/api/user/register', {
          username: this.registerForm.username,
          email: this.registerForm.email,
          password: this.registerForm.password,
          role: this.registerForm.role
        })

        if (response.data.code === 200) {
          this.$message.success('注册成功，请登录')
          this.switchToLogin()
        } else {
          this.$message.error(response.data.message || '注册失败')
        }
      } catch (error) {
        console.error('注册错误:', error)
        this.$message.error('注册失败，请检查网络连接')
      } finally {
        this.loading = false
      }
    },

    // 处理密码重置
    async handleReset() {
      try {
        await this.$refs.resetFormRef.validate()
        this.loading = true

        const response = await axios.post('/api/user/reset-password', {
          email: this.resetForm.email
        })

        if (response.data.code === 200) {
          this.$message.success('重置邮件已发送，请查收')
          this.switchToLogin()
        } else {
          this.$message.error(response.data.message || '发送失败')
        }
      } catch (error) {
        console.error('重置密码错误:', error)
        this.$message.error('发送失败，请检查网络连接')
      } finally {
        this.loading = false
      }
    }
  },
  
  created() {
    // 检查是否已登录
    const token = localStorage.getItem('token')
    if (token) {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.auth-content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  min-width: 400px;
  max-width: 500px;
}

.login-form,
.register-form,
.reset-form {
  text-align: center;
}

h2 {
  color: #333;
  margin-bottom: 30px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.el-form-item {
  margin-bottom: 25px;
}

.el-input {
  border-radius: 10px;
}

.el-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 10px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.el-button--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.auth-links {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

.auth-links .el-button--text {
  color: #667eea;
  font-weight: 500;
}

.auth-links .el-button--text:hover {
  color: #764ba2;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .auth-content {
    min-width: 90%;
    padding: 30px 20px;
  }
  
  .auth-links {
    flex-direction: column;
    gap: 10px;
  }
}
</style>