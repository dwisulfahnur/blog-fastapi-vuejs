<template>
  <div id="app">
    <nav class="navbar navbar-expand-sm bg-light">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link :to="{name: 'user-create'}" class="nav-link">New User</router-link>
        </li>
        <li class="nav-item">
          <router-link :to="{name: 'user-list'}" class="nav-link">User List</router-link>
        </li>
      </ul>
    </nav>

    <transition name="fade">
      <div class="gap">
        <div class="container mt-4">
          <router-view></router-view>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {};
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-active {
  opacity: 0;
}
</style>