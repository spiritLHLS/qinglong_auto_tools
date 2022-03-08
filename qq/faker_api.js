//国内机子解决无法直接给api发信息的需求
//反代网址：https://dash.cloudflare.com/
//注册后点右下角的worker，创建worker，把下面代码部署后点返回，重命名自己需要的前缀
//代理后的api:
//worker的名字你刚刚改的前缀.你的用户名.workers.dev
//等效于在国外机子里api.telegram.org使用
//作者仓库:https://github.com/spiritLHL/qinglong_auto_tools
//觉得不错麻烦点个star谢谢
//cloudfare的worker反代的api代码，下面填tg机器人API即可
const whitelist = ["/botxxxxx:xxxxxxxxxxx"];
const tg_host = "api.telegram.org";

addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})

function validate(path) {
    for (var i = 0; i < whitelist.length; i++) {
        if (path.startsWith(whitelist[i]))
            return true;
    }
    return false;
}

async function handleRequest(request) {
    var u = new URL(request.url);
    u.host = tg_host;
    if (!validate(u.pathname))
        return new Response('Unauthorized', {
            status: 403
        });
    var req = new Request(u, {
        method: request.method,
        headers: request.headers,
        body: request.body
    });
    const result = await fetch(req);
    return result;
}
