<template>
    <td class="player-tile">
        <p v-if="active">{{ pointValue }}</p>
        <p v-else>Not active</p>
    </td>
</template>

<script>
export default {
    name: "PlayerTile",
    props: {
        active: Boolean,
        pointValue: String
    }
}
</script>

<style>

</style>