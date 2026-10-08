// Regenerate favicons, logo-mark and the OG image: run `node tools/asset-saver.js` and `node tools/serve.js`,
// open http://localhost:8411/tools/assets.html, then convert icons/og-image.png to og-image.jpg (sips -s format jpeg).
const http=require('http'),fs=require('fs'),path=require('path');
const out=path.resolve(__dirname,'..','icons');
const allowed={'favicon-32x32.png':'favicons','favicon-16x16.png':'favicons','apple-touch-icon.png':'favicons','android-chrome-192x192.png':'favicons','logo-mark.png':'','og-image.png':''};
http.createServer((req,res)=>{
  res.setHeader('access-control-allow-origin','*');
  if(req.method==='OPTIONS'){res.writeHead(204,{'access-control-allow-headers':'content-type'});return res.end();}
  const name=new URL(req.url,'http://x').searchParams.get('name');
  if(req.method!=='POST'||!(name in allowed)){res.writeHead(400);return res.end('bad');}
  let b='';req.on('data',c=>b+=c);req.on('end',()=>{
    const buf=Buffer.from(b.replace(/^data:image\/png;base64,/,''),'base64');
    fs.writeFileSync(path.join(out,allowed[name],name),buf);res.end('ok '+buf.length);});
}).listen(8412,()=>console.log('saver on 8412'));
