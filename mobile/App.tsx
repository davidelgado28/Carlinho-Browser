import React,{useRef,useState} from 'react';
import {SafeAreaView,StyleSheet,Text,TextInput,TouchableOpacity,View} from 'react-native';
import {WebView} from 'react-native-webview';
const HOME='https://example.com';
export default function App(){
 const web=useRef<WebView>(null); const [url,setUrl]=useState(HOME);
 return <SafeAreaView style={styles.root}><View style={styles.toolbar}>
  <TouchableOpacity onPress={()=>web.current?.goBack()}><Text style={styles.button}>‹</Text></TouchableOpacity>
  <TouchableOpacity onPress={()=>web.current?.goForward()}><Text style={styles.button}>›</Text></TouchableOpacity>
  <TextInput style={styles.address} value={url} onChangeText={setUrl} onSubmitEditing={()=>web.current?.injectJavaScript(`location.href=${JSON.stringify(url)};true;`)} autoCapitalize="none" autoCorrect={false} keyboardType="url"/>
  <TouchableOpacity onPress={()=>web.current?.reload()}><Text style={styles.button}>⟳</Text></TouchableOpacity>
 </View><WebView ref={web} source={{uri:HOME}} sharedCookiesEnabled={false} thirdPartyCookiesEnabled={false} cacheEnabled={false} javaScriptEnabled domStorageEnabled={false} onNavigationStateChange={s=>setUrl(s.url)}/></SafeAreaView>;
}
const styles=StyleSheet.create({root:{flex:1,backgroundColor:'#050505'},toolbar:{height:54,flexDirection:'row',alignItems:'center',paddingHorizontal:8,gap:6,backgroundColor:'#050505'},button:{color:'#fff',fontSize:28,width:28,textAlign:'center'},address:{flex:1,height:40,borderRadius:10,backgroundColor:'#111',color:'#fff',paddingHorizontal:12}});
