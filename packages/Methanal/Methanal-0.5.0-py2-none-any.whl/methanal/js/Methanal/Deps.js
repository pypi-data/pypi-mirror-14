// import Methanal.Preds
// import Methanal.Util
Methanal.Deps.oneOf = function oneOf(values) {
    Divmod.warn(
        'Methanal.Deps is deprecated, use Methanal.Preds',
        Divmod.DeprecationWarning);
    return Methanal.Preds.oneOf(values);
};
