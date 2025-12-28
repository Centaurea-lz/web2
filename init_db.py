import random
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from app import create_app, db
from app.models import User, Movie, Tag, Review
app = create_app()
# 假设在 routes.py 中
from flask import render_template, request
from app import db
from app.models import Movie


@app.route('/')


def init_db():
    with app.app_context():
        # 删除旧表（开发环境）
        db.drop_all()
        # 创建新表
        db.create_all()

        # 1. 预填充标签
        tag_names = ['科幻', '悬疑', '喜剧', '爱情', '动作', '恐怖', '动画', '纪录片']
        tags = []
        for name in tag_names:
            tag = Tag(name=name)
            db.session.add(tag)
            tags.append(tag)
        db.session.commit()

        # 2. 预填充电影（含标签关联）
        movies_data = [
            {
                "title": "星际穿越",
                "release_year": 2014,
                "description": "未来地球黄沙遍野，农作物因枯萎病灭绝，宇航员库珀穿越虫洞为人类寻找新家园，在时空悖论中诠释父爱与责任。",
                "poster_url": "Interstellar.jpg",
                "tags": [tags[0], tags[1]]  # 科幻、悬疑
            },
            {
                "title": "这个杀手不太冷",
                "release_year": 1994,
                "description": "职业杀手里昂偶遇全家被灭门的少女玛蒂尔达，两人从互相戒备到相依为命，在黑白两道的追杀中绽放出畸形却温暖的情感。",
                "poster_url": "Leon.jpg",
                "tags": [tags[4], tags[3]]  # 动作、爱情
            },
            {
                "title": "千与千寻",
                "release_year": 2001,
                "description": "千寻随父母误入神灵异世界，父母因贪吃变成猪，为拯救家人，千寻在汤婆婆的澡堂打工，逐渐从怯懦少女成长为独立勇敢的个体。",
                "poster_url": "Spirited Away.jpg",
                "tags": [tags[6], tags[0]]  # 动画、科幻
            },
            {
                "title": "让子弹飞",
                "release_year": 2010,
                "description": "悍匪张牧之化身县长马邦德，与鹅城恶霸黄四郎展开殊死较量，在嬉笑怒骂间揭露了旧时代的权力腐败与阶级矛盾。",
                "poster_url": "Let The Bullets Fly.jpg",
                "tags": [tags[4], tags[2]]  # 动作、喜剧
            },
            {
                "title": "霸王别姬",
                "release_year": 1993,
                "description": "程蝶衣与段小楼自幼学戏，一人成虞姬一人为霸王，半生纠缠在戏梦与现实、个人命运与时代洪流的漩涡中，谱写梨园悲歌。",
                "poster_url": "Farewell My Concubine.jpg",
                "tags": [tags[3], tags[1]]  # 爱情、悬疑
            },
            {
                "title": "颂乐人偶 BanG Dream! Ave Mujica",  # 电影标题
                "release_year": 2025,  # 上映年份
                "description": "我没说过吗？请把你剩下的人生交给我\n"
                               "由丰川祥子招募成员的乐队Ave Mujica，通过现场演出和媒体曝光等，取得了商业上的成功。\n"
                               "曾经发誓与命运同行的伙伴们，还有出生和成长家园都失去了的少女。\n"
                               "她是为了什么而背负着他人的生活的重担，并延续着乐队的发展？\n"
                               "过去也好，真实的面目也好，都用面具掩盖起来，今晚她也伫立在这完美的箱庭中。 ",
                "poster_url": "AVE Mujica.jpg",  # 海报文件名（需放到 static/posters/ 目录）
                "tags": [tags[5], tags[6],tags[2],tags[3]]  # 关联标签（从已有的 tag_names 中选择，如 tags[0] 对应科幻）
            },
            {
                "title": "迷途之子!!!!! BanG Dream! It's MyGO!!!!!",
                "release_year": 2023,
                "description": "你能，和我组一辈子乐队吗？"
                               "高一的春末。羽丘女子学园里的学生基本上都组好了乐队， "
                               "推迟入学的爱音也在为了能尽快融入班级而急忙寻找乐队成员。"
                               "在这时候，知道「羽丘的小怪人」灯还没组乐队之后， "
                               "爱音不由自主地向她搭话…… "
                               "遍体鳞伤且蓬头垢面的，我们的“音乐（呐喊）"
                               "不畏迷茫，纵使迷茫亦要前行",
                "poster_url": "Mygo.jpg",
                "tags": [tags[3], tags[6]]
            },
            {
                "title": "颐和园",
                "release_year": 2010,
                "description": "两度寒暑的大型拍摄，震撼奢华的视觉盛宴，揭秘一座皇家园林的前世今生。"
                               "特技、再现，复活清漪园久已消失的绝世风景；"
                               "故事、人物，描摹颐和园风云变幻的皇家生活。 ",
                "poster_url": "Yiheyuan.jpg",
                "tags": [tags[7]]
            },
            {
                "title": "死神来了 Final Destination",
                "release_year": 2000,
                "description": "剧情惊险恐怖，环环相扣。高中生艾利克斯-伯朗宁（德文•萨瓦 Devon Sawa 饰）与7名同班同学登机前往巴黎。"
                               "起飞前，他突然预感到恐怖的一幕：飞机将会在空中爆炸。"
                               "艾利克斯非常惊恐，大喊飞机即将出事，大家要立刻下机，"
                               "结果混乱中他和其余6名乘客被机组人员赶了出来。"
                               "但是，被艾利克斯不幸言中，飞机在半空中爆炸，全部人员罹难。"
                               "所有下了机的人都在庆幸大难不死，却不知死神还是不愿放过他们。"
                               "接下来，等待他们的将会是更恐怖的死亡方式和更难逃脱的死亡命运。"
                               "而艾利克斯又能从各人的死亡顺序里面发现什么秘密，在死神的魔爪中逃出生天？",
                "poster_url": "Final Destination.jpg",
                "tags": [tags[5]]
            },
            {
                "title": "007：无暇赴死 No Time to Die",
                "release_year": 2021,
                "description": "世界局势波诡云谲，再度出山的邦德（丹尼尔·克雷格 饰）面临有史以来空前的危机，"
                               "传奇特工007的故事在本片中达到高潮。新老角色集结亮相，蕾雅·赛杜回归，"
                               "二度饰演邦女郎玛德琳。系列最恐怖反派萨芬（拉米·马雷克 饰）重磅登场，"
                               "毫不留情地展示了自己狠辣的一面，不仅揭开了玛德琳身上隐藏的秘密，"
                               "还酝酿着危及数百万人性命的阴谋，幽灵党的身影也似乎再次浮出水面。"
                               "半路杀出的新00号特工（拉什纳·林奇 饰）与神秘女子（安娜·德·阿玛斯 饰）看似与邦德同阵作战，"
                               "但其真实目的依然成谜。关乎邦德生死的新仇旧怨接踵而至，"
                               "暗潮汹涌之下他能否拯救世界？",
                "poster_url": "notimetodie.jpg",
                "tags": [tags[0], tags[4]]
            },
            {
                "title": "虎口脱险 La grande vadrouille",
                "release_year": 1966,
                "description": "二战期间，英国一架飞机在执行轰炸任务中，被德军击中，几名英国士兵被迫跳伞逃生."
                               "他们约好在土耳其浴室见面，并用这次行动的代号“鸳鸯茶”作为接头暗号。"
                               "他们分别降落在法国巴黎德军占领区的不同地点。大胡子中队长雷金纳德被动物园管理员所救。"
                               "而另外两名士兵，也分别在油漆匠奥古斯德 （布尔维尔 饰）"
                               "和乐队指挥斯塔尼斯拉斯（路易·德·费内斯 饰）的帮助下掩藏好了。"
                               "即便德军展开了全城的搜索，油漆匠、指挥和中队长还是在浴室顺利地会面，"
                               "几经辗转，英国士兵终于接上了头。几个原本并不认识的人，就这样结成了生死同盟，"
                               "与敌人展开了斗智斗勇的生死游戏。同时，也闹出了不少温情的笑话。"
                               "他们用微薄的力量对抗严 n酷德军，险相迭生，滑稽搞笑，为了逃出虎口，共同战斗。",
                "poster_url": "La grande vadrouille.jpg",
                "tags": [tags[2]]
            },
            {
                "title": "魂断蓝桥 Waterloo Bridge",
                "release_year": 1940,
                "description": "　第一次世界大战期间，回国度假的陆军中尉罗伊（罗伯特·泰勒）在滑铁卢桥上邂逅了舞蹈演员玛拉（费雯·丽），"
                               "两人彼此倾心，爱情迅速升温。就在两人决定结婚之时，罗伊应招回营地，两人被迫分离。"
                               "由于错过剧团演出，玛拉被开除，只能和好友相依为命。不久玛拉得知罗伊阵亡的消息，"
                               "几欲崩溃，备受打击。失去爱情的玛拉感到一切都失去了意义，为了生存，"
                               "她和好友不得不沦为妓女。然而命运弄人，就在此时玛拉竟然再次遇到了罗伊。"
                               "虽然为罗伊的生还兴奋不已，玛拉却因自己的失身陷入痛苦之中。"
                               "感到一切难以挽回的玛拉潸然离开，独自来到两人最初相遇的地点——滑铁卢桥上…",
                "poster_url": "Waterloo Bridge.jpg",
                "tags": [tags[3]]
            },
            {
                "title": "功夫",
                "release_year": 2004,
                "description": "1940年代的上海，自小受尽欺辱的街头混混阿星（周星驰）为了能出人头地，"
                               "可谓窥见机会的缝隙就往里钻，今次他盯上行动日益猖獗的黑道势力“斧头帮”，"
                               "想借之大名成就大业。阿星假冒“斧头帮”成员试图在一个叫“猪笼城寨”的地方对居民敲诈，"
                               "不想引来真的“斧头帮”与“猪笼城寨”居民的恩怨。“猪笼城寨”原是藏龙卧虎之处，"
                               "居民中有许多身怀绝技者（元华、梁小龙等），他们隐藏于此本是为远离江湖恩怨，"
                               "不想麻烦自动上身，躲都躲不及。而在观战正邪两派的斗争中，阿星逐渐领悟功夫的真谛。",
                "poster_url": "Kung Fu Hustle.jpg",
                "tags": [tags[2], tags[4]]
            },
            {
                "title": "速度与激情5 Fast Five",
                "release_year": 2011,
                "description": "蛰伏2年之后，多姆(范·迪塞尔 Vin Diesel饰)与布莱恩(保罗`沃克 Paul Walker 饰)再度联手把火车中的神秘豪车盗走，"
                               "遭到了警察和黑帮分子的火线追杀。布莱恩和米娅(乔丹娜·布鲁斯特 Jordana Brewster 饰)到里约寻找援兵，"
                               "并与多姆会和。为了寻找多米等人的下落，FBI王牌探员卢克(“巨石”道恩·强森 Dwayne Johnson饰）挺身而出，"
                               "组成精英部队，追查来到里约。他雇佣了丧夫的美丽女警艾莲娜(埃尔莎`帕塔奇 Elsa Pataky 饰)，一同寻找多姆。"
                               "与此同时，里约的地头蛇也对这些不速之客开火，三股势力开始相互缠斗。期间，因米娅怀孕，"
                               "布莱恩决定陪她一起逃亡，所以多姆只得依靠昔日老友探寻新车的秘密。在罗曼、韩等人的帮助下，"
                               "多姆终于找到了这辆车的秘密——芯片，并由此揭开了其中隐藏的一个不可告人的计划……",
                "poster_url": "Fast Five.jpg",
                "tags": [tags[4]]
            },
            {
                "title": "神探夏洛克 第一季",
                "release_year": 2010,
                "description": "《神探夏洛克》是一部由BBC出品的英国迷你电视剧，该剧将原著的故事背景从19世纪大英帝国国势鼎盛的时"
                               "期搬到了21世纪繁华热闹的大都市中。这一次夏洛克·福尔摩斯(本尼迪克特·康伯巴奇 Benedict Cumberbatch 饰)"
                               "不仅是著名大侦探更是一名时尚潮人。和他的 好友兼得力助手约翰·华生（马丁·弗瑞曼 Martin Freeman 饰）"
                               "分别经历了离奇市民自杀案件、黑帮走私事件和倒计时炸弹杀人案。每一个案件看似独立其实都有联系"
                               "，两人每解决一个案子，就又会出现新的难题和的受害无辜百姓。经过抽丝剥茧，"
                               "幕后黑手莫里亚蒂(安德鲁·斯科特 Andrew Scott 饰)终于浮出水面，最后一集的交锋中，"
                               "被炸弹和狙击枪威胁的夏洛克和华生该如何脱身，只能等到第二季让BBC来告诉大家了。",
                "poster_url": "Sherlock Season 1.jpg",
                "tags": [tags[1]]
            },
            {
                "title": "二战中的指挥官",
                "release_year": 2009,
                "description": "这部全新的二战纪录片从一个全新的角度探讨了二战中的著名战役。比较了交战双方指挥官的军事策略、面对的困境以及失败。"
                               "我们探究了他们试图在计谋上打败对方时采取的行动以及迎敌方案。讲述的战役包括二战中具有转折意义的战役："
                               "新加坡战役、阿拉曼之战、库尔斯克战役、斯大林格勒战役、中途岛之战。"
                               "传奇的指挥官包括：隆美尔、蒙哥马利、曼斯坦因等。"
                               "本片用全新、独特而且直观的表现手法，从战场指挥官的角度诠绎了二战中的几场著名战役。 ",
                "poster_url": "Generals at War.jpg",
                "tags": [tags[7]]
            },
            {
                "title": "賭神",
                "release_year": 1989,
                "description": "高进（周润发 饰）前来香港与赌魔决斗，怎料刚抵港，便被南哥（杨泽霖 饰）追杀，结果堕入陷阱而失忆。"
                               "幸得刀仔（刘德华 饰）和其女友珍（王祖贤 饰）相救，他们把高进带回家中疗养，发现高进精通赌术后，"
                               "兴奋不已，想利用他来挣大钱，却反而因为高进发挥不稳亏了钱。高进妻子遭其堂弟 高义醉酒后污辱杀害。"
                               "高义进而联手南哥，设计谋害高进，四处搜罗进的藏身地点，前往追杀。逃亡之时，高进翻车受伤，"
                               "竟恢复了记忆——但是却怎样也记不起失忆期间的事情。刀仔提醒进，高义并非好人，但进却已然蒙在鼓里，"
                               "不知危难当头。",
                "poster_url": "God of Gamblers.jpg",
                "tags": [tags[1]]
            },
            {
                "title": "金玉滿堂",
                "release_year": 1995,
                "description": "赵港生（张国荣饰）因厌烦黑社会生活，欲金盆洗手后去加拿大追寻偶像山口百惠，而他选择的移民途径竟是——"
                               "参加加拿大酒店的厨师考试，丝毫不懂厨艺的他最终因作弊暴露而惨败。某日，赵港生在酒楼遇见了厨艺大师龙昆宝"
                               "（赵文卓饰），龙昆宝指点他去找自己的旧识满汉楼的欧老板（罗家英饰）学习，不想欧老板竟对他百般刁难，"
                               "最终将其扫地出门。其间，港生和欧老板的女儿嘉惠（袁咏仪饰）倒是在不经意间擦出了花火。"
                               "欧老板师承中国著名大宴满汉全席之赵派，某日，牛派的继承人黄荣找上门来挑战，"
                               "后来又使诡计挖走了他手下的所有师傅。这时，唯有港生挺身而出，和嘉惠一起寻找会做满汉全席的高人，"
                               "那就是五年前莫名隐退厨艺界的廖杰（钟镇涛饰）。",
                "poster_url": "The Chinese Feast.jpg",
                "tags": [tags[2], tags[3]]
            },
            {
                "title": "鲁邦三世：鲁邦VS复制人",
                "release_year": 1978,
                "description": "鲁邦终于被捕了，他的结局是上绞刑架被处死，医学报告证实了这个已经被处死的犯人正是鲁邦本人。然而钱形警部深信死了的这个绝不是真正的鲁邦……"
                               "本作为鲁邦三世第一部剧场版，于1978年12月16日上映。 ",
                "poster_url": "lbss.jpg",
                "tags": [tags[1], tags[6]]
            }

        ]

        movies = []
        for data in movies_data:
            movie = Movie(
                title=data["title"],
                release_year=data["release_year"],
                description=data["description"],
                poster_url=data["poster_url"],
                tags=data["tags"]
            )
            db.session.add(movie)
            movies.append(movie)
        db.session.commit()

        # 3. 创建测试用户
        test_user = User(
            username="testuser",
            email="test@example.com"
        )
        test_user.set_password("123456")
        db.session.add(test_user)
        db.session.commit()

        # 4. 预填充评论
        review_contents = [
            "剧情震撼，星际穿越的物理设定很严谨，父爱线太好哭了！",
            "里昂的盆栽和牛奶，是杀手的温柔底色，结局意难平。",
            "宫崎骏的想象力太绝了，千寻的成长治愈了很多人。",
            "姜文的黑色幽默，每个镜头都有隐喻，百看不厌。",
            "不疯魔不成活，程蝶衣的一生都是一场盛大的戏。",
            "离神还有距离，离人已经很远了。",
            "咕咕嘎嘎"
        ]

        for i in range(len(review_contents)):
            review = Review(
                content=review_contents[i],
                rating=random.randint(4, 5),
                user_id=test_user.id,
                movie_id=movies[i].id
            )
            db.session.add(review)
        db.session.commit()

        # 5. 测试用户点赞电影
        test_user.liked_movies.append(movies[0])
        test_user.liked_movies.append(movies[2])
        db.session.commit()

        print("✅ 数据库初始化完成！测试用户：testuser，密码：123456")

if __name__ == "__main__":
    init_db()
