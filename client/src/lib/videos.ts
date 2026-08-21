/**
 * Design: Warm Code Studio — a single editorial data source for archive, search, and detail routes.
 */
export type VideoTopic = "الكل" | "الأساسيات" | "إدارة الحالة" | "واجهة المستخدم" | "واجهات API";

export type VideoRecord = {
  id: string;
  topic: Exclude<VideoTopic, "الكل">;
  title: string;
  description: string;
  concept: string;
  duration: string;
  signal: string;
  accent: "amber" | "blue" | "red";
  status: "جاهز للمشاهدة" | "سكربت جاهز";
  available: boolean;
  script: string[];
  code: string;
  takeaway: string;
};

export const archiveTopics: VideoTopic[] = ["الكل", "الأساسيات", "إدارة الحالة", "واجهة المستخدم", "واجهات API"];

export const videos: VideoRecord[] = [
  {
    id: "pubspec-yaml",
    topic: "الأساسيات",
    title: "ما وظيفة pubspec.yaml؟",
    description: "الحزم، الأصول، والإصدارات التي تضبط مشروعك من أول سطر.",
    concept: "dependencies assets flutter pub get",
    duration: "00:48",
    signal: "SDK / ASSETS",
    accent: "amber",
    status: "جاهز للمشاهدة",
    available: true,
    script: [
      "مرحبًا! إذا كنت تبدأ مشروع Flutter جديد، فهناك ملف مهم جدًا يجب أن تفهمه: pubspec.yaml.",
      "هذا الملف يعرّف اسم التطبيق ووصفه وإصداره، بالإضافة إلى نسخة Flutter أو Dart التي يعتمد عليها المشروع.",
      "والأهم أنك تستخدمه لإضافة الحزم، مثل provider أو http، وكذلك لتسجيل الصور والخطوط داخل مجلد assets.",
      "بعد تعديل الملف، شغّل flutter pub get حتى ينزّل Flutter الحزم ويحدّث المشروع.",
      "إذا ظهرت مشكلة في حزمة أو صورة أو خط، ابدأ دائمًا بمراجعة pubspec.yaml.",
    ],
    code: `name: my_flutter_app
environment:
  sdk: ">=3.2.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  provider: ^6.1.1
  http: ^1.2.1

flutter:
  uses-material-design: true
  assets:
    - assets/images/`,
    takeaway: "اعتبره لوحة التحكم للحزم، الإصدارات، والأصول في مشروعك.",
  },
  {
    id: "provider-state",
    topic: "إدارة الحالة",
    title: "ابدأ إدارة الحالة بـ Provider",
    description: "متى تستخدم ChangeNotifier وConsumer لتحديث الواجهة بوضوح؟",
    concept: "provider state management ChangeNotifier Consumer notifyListeners",
    duration: "00:45",
    signal: "STATE / PROVIDER",
    accent: "blue",
    status: "سكربت جاهز",
    available: false,
    script: [
      "هل واجهت مشكلة أن أكثر من شاشة في تطبيق Flutter تحتاج إلى نفس البيانات؟ هنا يأتي دور Provider.",
      "Provider يساعدك على مشاركة الحالة بين الواجهات بدل تمرير البيانات يدويًا من شاشة إلى أخرى.",
      "عرّف كلاس للحالة، واجعله يرث من ChangeNotifier، ثم استدعِ notifyListeners عندما تتغير البيانات.",
      "اربط الكلاس بالتطبيق عبر ChangeNotifierProvider، ثم استخدم Consumer داخل الواجهة التي تحتاج التحديث.",
      "باختصار: Provider يفصل منطق التطبيق عن الواجهة ويجعل الكود أوضح وأسهل في الصيانة.",
    ],
    code: `class CounterState extends ChangeNotifier {
  int value = 0;

  void increment() {
    value++;
    notifyListeners();
  }
}

ChangeNotifierProvider(
  create: (_) => CounterState(),
  child: const MyApp(),
);`,
    takeaway: "ضع الحالة في مكان واحد، واسمح للواجهات أن تستمع إلى التغيير فقط عند الحاجة.",
  },
  {
    id: "provider-vs-riverpod",
    topic: "إدارة الحالة",
    title: "Provider أم Riverpod؟",
    description: "اختيار عملي حسب حجم المشروع وطريقة تنظيم الاعتماديات.",
    concept: "Provider Riverpod state management dependency injection",
    duration: "00:52",
    signal: "STATE / CHOICE",
    accent: "red",
    status: "سكربت جاهز",
    available: false,
    script: [
      "Provider وRiverpod يحلان مشكلة إدارة الحالة، لكن طريقة الاستخدام تختلف.",
      "Provider خيار مباشر وواضح إذا كنت تبدأ بتطبيق صغير أو تريد نمطًا معروفًا وبسيطًا داخل شجرة الواجهات.",
      "Riverpod يقدّم أسلوبًا مستقلًا عن BuildContext، ما يساعد في الاختبار وتنظيم الاعتماديات عندما يكبر المشروع.",
      "لا تبحث عن فائز مطلق. اختر الأداة التي يستطيع فريقك قراءتها وصيانتها بثقة.",
    ],
    code: `// Provider: read from BuildContext
final count = context.watch<CounterState>().value;

// Riverpod: read from a ref
final count = ref.watch(counterProvider);`,
    takeaway: "ابدأ ببساطة، ثم اختر النمط الذي يحافظ على وضوح مشروعك مع نموه.",
  },
  {
    id: "form-validation",
    topic: "واجهة المستخدم",
    title: "تحقق تسجيل الدخول",
    description: "Form وGlobalKey وTextFormField من دون تعقيد أو تكرار.",
    concept: "Form GlobalKey TextFormField validation login UI",
    duration: "00:45",
    signal: "UI / FORM",
    accent: "blue",
    status: "سكربت جاهز",
    available: false,
    script: [
      "لا ترسل بيانات تسجيل الدخول قبل أن تتحقق منها داخل الواجهة.",
      "أنشئ GlobalKey واحدًا للـ Form، ثم أضف validator لكل TextFormField يحتاج إلى قاعدة واضحة.",
      "عند الضغط على زر الدخول، استدعِ validate. إذا كانت النتيجة صحيحة، انتقل إلى طلب API. وإذا لم تكن كذلك، دع الحقل يشرح الخطأ للمستخدم.",
      "هذه الخطوة الصغيرة تمنحك واجهة أكثر هدوءًا ورسائل أخطاء أوضح.",
    ],
    code: `final formKey = GlobalKey<FormState>();

TextFormField(
  validator: (value) {
    if (value == null || !value.contains('@')) {
      return 'أدخل بريدًا صحيحًا';
    }
    return null;
  },
);

if (formKey.currentState!.validate()) {
  // submit credentials
}`,
    takeaway: "تحقق من الإدخال قبل الشبكة؛ ذلك يوفر أخطاء أقل وتجربة أوضح.",
  },
  {
    id: "dio-api",
    topic: "واجهات API",
    title: "API أنظف باستخدام Dio",
    description: "تحميل، أخطاء، وتحويل JSON إلى Model بصورة منظمة.",
    concept: "Dio API JSON model loading error handling Flutter",
    duration: "01:00",
    signal: "API / DIO",
    accent: "amber",
    status: "سكربت جاهز",
    available: false,
    script: [
      "عند ربط Flutter بواجهة API، لا تضع طلب الشبكة مباشرة داخل الواجهة.",
      "أنشئ خدمة صغيرة تستخدم Dio، واجعلها مسؤولة عن إرسال الطلب ومعالجة الاستجابة.",
      "حوّل البيانات القادمة إلى Model بدل تمرير Map في كل مكان، وتعامل مع حالة التحميل والخطأ بشكل صريح.",
      "بهذا يبقى Widget مسؤولًا عن العرض، وتبقى طبقة الشبكة مسؤولة عن البيانات.",
    ],
    code: `final dio = Dio();

Future<User> getUser() async {
  final response = await dio.get('/users/1');
  return User.fromJson(response.data);
}`,
    takeaway: "افصل الشبكة عن الواجهة، ثم حوّل الاستجابة إلى نموذج واضح قابل للاختبار.",
  },
  {
    id: "column-listview",
    topic: "واجهة المستخدم",
    title: "متى تستخدم Column وListView؟",
    description: "قاعدة صغيرة تساعدك على منع مشاكل التمرير وتضارب المساحات.",
    concept: "Column ListView scroll layout viewport Flutter UI",
    duration: "00:38",
    signal: "UI / LAYOUT",
    accent: "red",
    status: "سكربت جاهز",
    available: false,
    script: [
      "استخدم Column عندما يكون لديك عدد محدود من العناصر ولا تحتاج إلى تمرير طويل.",
      "أما إذا كانت القائمة قابلة للنمو أو يجب أن يتمرر محتواها، فابدأ بـ ListView.",
      "المشكلة الشائعة هي وضع ListView داخل Column دون مساحة محددة. الحل عادة يكون Expanded أو shrinkWrap حسب السياق.",
      "اختيار Widget الصحيح من البداية يمنع أخطاء overflow ويجعل الواجهة أكثر سلاسة.",
    ],
    code: `Column(
  children: [
    const Header(),
    Expanded(
      child: ListView.builder(
        itemCount: items.length,
        itemBuilder: (_, index) => Text(items[index]),
      ),
    ),
  ],
)`,
    takeaway: "محتوى محدود؟ Column. محتوى قابل للتمرير؟ ListView مع مساحة واضحة.",
  },
];

export function getVideoById(id: string) {
  return videos.find((video) => video.id === id);
}
