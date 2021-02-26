<template>
    <div id="app">
        <Nav/>

        <transition name="fade">
            <div class="gap">
                <div class="container mt-4 d-flex justify-content-center">
                    <router-view></router-view>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
    import Nav from "./components/Nav";

    export default {
        components: {Nav}
    };
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