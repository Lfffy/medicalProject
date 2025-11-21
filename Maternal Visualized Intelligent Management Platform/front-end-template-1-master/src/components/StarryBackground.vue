<template>
  <div id="background-container">
    <div class="maternal-pattern"></div>
    <div class="gradient-overlay"></div>
  </div>
</template>

<script>
export default {
  data(){
    return {
    }
  },
  components: {
  },
};
</script>

<style>
#background-container {
  width: 100vw;
  min-height: 100vh;
  position: absolute;
  z-index: -1;
  background: linear-gradient(135deg, #fff5f7 0%, #ffe6ec 50%, #ffd8e3 100%);
  overflow: hidden;
}

.maternal-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(#ffb6c1 1px, transparent 1px),
    radial-gradient(#ffb6c1 1px, transparent 1px);
  background-size: 40px 40px;
  background-position: 0 0, 20px 20px;
  opacity: 0.2;
  animation: float 20s ease-in-out infinite;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.5) 100%);
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(1deg);
  }
}
</style>