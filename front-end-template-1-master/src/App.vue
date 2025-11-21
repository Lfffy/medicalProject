<template>
  <div id="app">
    <StarryBackground/>
    <UnifiedLayout />
  </div>
</template>

<script>
import StarryBackground from './components/StarryBackground'
import UnifiedLayout from './components/UnifiedLayout'

export default {
  name: 'App',
  components: {
    StarryBackground,
    UnifiedLayout
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  overflow-x: hidden;
}

body {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: #fff5f7;
}

#app {
  height: 100%;
}

/* 全局过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Element UI 样式覆盖 */
.el-card {
  border-radius: 12px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
  border: none !important;
}

.el-button--primary {
  background: linear-gradient(135deg, #ff7eb3 0%, #ff66a3 100%) !important;
  border: none !important;
  
  &:hover {
    background: linear-gradient(135deg, #ff66a3 0%, #ff5599 100%) !important;
  }
}

.el-tabs__item.is-active {
  color: #ff66a3 !important;
}

.el-tabs__active-bar {
  background-color: #ff66a3 !important;
}

.el-input__inner:focus {
  border-color: #ff66a3 !important;
}

.el-select .el-input.is-focus .el-input__inner {
  border-color: #ff66a3 !important;
}
</style>
