import React from 'react';
import { FlatList, StyleSheet, Text, View, Button, ListRenderItemInfo } from 'react-native';
import { BleManager, Device, BleError } from 'react-native-ble-plx';

class SetupPage extends React.Component<any, {device?: Device | null, wifi: string[]}> {
    manager: BleManager;
    device?: Device;

    constructor(props: any) {
        super(props);
        this.manager = new BleManager();
        this.state = {wifi: [], device: null};
    }

    componentWillUnmount(){
        this.manager.destroy();
        this.scanAndConnect();
    }

    connect(wifi: string){

    }

    scanAndConnect() {
        this.manager.startDeviceScan(null, null, (error: BleError | null, device: Device | null) => {
            if (error || device === null) {
                // Handle error (scanning will be stopped automatically)
                return
            }
    
            // Check if it is a device you are looking for based on advertisement data
            // or other criteria.
            if (device.name === 'raspberrypi') {
                this.manager.stopDeviceScan();
    
                device.connect()
                    .then((device) => {
                        return device.discoverAllServicesAndCharacteristics()
                    })
                    .then((device) => {
                        
                    })
                    .catch((error) => {
                        // Handle errors
                    });
            }
        });
    }

    render(){
        return (
            <View style={styles.container}>
                <FlatList 
                    data={this.state.wifi}
                    renderItem={(deviceInfo: ListRenderItemInfo<string>) => {
                        return (
                            <Button 
                                title={deviceInfo.item} 
                                onPress={() => this.connect(deviceInfo.item)}
                            />)
                    }}
                ></FlatList>
                <Text>HELLO HELLO THIS IS A TEST</Text>
            </View>
        )
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#FFF',
        alignItems: 'center',
        justifyContent: 'center',
    }
})
