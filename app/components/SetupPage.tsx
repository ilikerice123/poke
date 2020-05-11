import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

export default function SetupPage() {
    return (
        <View style={styles.container}>
            <Text>HELLO HELLO THIS IS A TEST</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#FFF',
        alignItems: 'center',
        justifyContent: 'center',
    }
})
