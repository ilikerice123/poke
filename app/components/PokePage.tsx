import React from 'react';
import { StyleSheet, Text, View, TextInput, Button, ActivityIndicator, ToastAndroid } from 'react-native';

const SERVER_URL = 'http://ec2-54-245-184-188.us-west-2.compute.amazonaws.com:8000'
export default function PokePage() {
    const [id, setId] = React.useState('')
    return (
        <View style={styles.container}>
            <TextInput
                multiline
                onChangeText={setId}
                value={id}
                placeholder={'enter id of poke light'}
            />
            <LoadButton
                id={id}
                // onPress={() => sendPoke(id)}
                title="Send Poke"
                color={'pink'}
            />
        </View>
    );
}

function LoadButton(props: any){
    const [loading, setLoading] = React.useState(false) 

    return(
        loading ? 
            <ActivityIndicator animating={loading} size="large" color='#FFC0CB' /> :
            <Button 
                onPress={() => sendPoke(props.id, setLoading)}
                title={'Send Poke'}
                color={'pink'}
            />
    )
}

function sendPoke(id: String, toggle: (b: boolean) => any){
    toggle(true)
    fetch(`${SERVER_URL}/devices/${id}/poke`, {method: 'POST'})
        .then((response) => {
            toggle(false)
            ToastAndroid.showWithGravity("Successfully sent poke", ToastAndroid.SHORT, ToastAndroid.CENTER)
        })
        .catch((error) => {
            toggle(false)
            ToastAndroid.showWithGravity("Error occurred", ToastAndroid.SHORT, ToastAndroid.CENTER)
        })
    return id
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#FFF',
        alignItems: 'center',
        justifyContent: 'center',
    },
    textInput: {
        height: '100px',
        color: 'pink',
        backgroundColor: '#FFC0CB',
        borderColor: 'gray',
        borderWidth: 3
    }
});
