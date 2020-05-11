import React from 'react';
import { StyleSheet, View, TextInput, Button, ActivityIndicator, ToastAndroid, Text } from 'react-native';
//import AsyncStorage from '@react-native-community/async-storage';
import { AsyncStorage } from 'react-native'

const SERVER_URL = 'http://ec2-54-245-184-188.us-west-2.compute.amazonaws.com:8000'
export default function PokePage() {
    const [code, setCode] = React.useState('')
    const [id, setId] = React.useState('loading...')
    loadId()
        .then((value) => {
            setId(value || "error occured")
        })
        .catch(() => {
            setId("error occurred")
        })
    return (
        <View style={styles.container}>
            <Text>The current id for this poke is {id}</Text>
            <TextInput
                multiline
                onChangeText={setCode}
                value={code}
                placeholder={'Enter verification code of light'}
            />
            <AsyncButton
                url={`${SERVER_URL}/devices/${code}/activate`}
                method={'POST'}
                afterRun={(data) => {
                    storeId(data.id)
                    setId(data.id)
                }}
                title={'verify'}
            />
            <AsyncButton
                url={`${SERVER_URL}/devices/${id}/poke`}
                method={'POST'}
                title={'send poke'}
                color={'pink'}
            />
        </View>
    );
}

function AsyncButton(props: {url: string, method: string, afterRun?: (res : any) => any, title?: string, color?: string}){
    const [loading, setLoading] = React.useState(false) 

    return(
        loading ? 
            <ActivityIndicator animating={loading} size="large" color='#FFC0CB' /> :
            <Button
                onPress={() => sendRequest(props.url, props.method, setLoading, props.afterRun)}
                title={props.title || 'button'}
                color={props.color}
            />
    )
}

function sendRequest(url: string, method: string, toggle: (b: boolean) => any, afterRun?: (res : any) => any){
    toggle(true)
    fetch(url, {method: method})
        .then((response) => {
            if(afterRun){
                afterRun(response)
            }
            toggle(false)
            ToastAndroid.showWithGravity("Successfully sent poke", ToastAndroid.SHORT, ToastAndroid.CENTER)
        })
        .catch((error) => {
            toggle(false)
            ToastAndroid.showWithGravity("Error occurred", ToastAndroid.SHORT, ToastAndroid.CENTER)
        })
}

async function loadId() {
    try {
        return await AsyncStorage.getItem("id")
    } catch(e) {
        console.log(e)
    }
}

async function storeId(value: string){
    try {
        return await AsyncStorage.setItem("id", value)
    } catch(e) {
        console.log(e)
    }
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
    },
});
