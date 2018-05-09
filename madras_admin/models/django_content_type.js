'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('django_content_type', {
    'app_label': {
      type: DataTypes.STRING,
    },
    'model': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'django_content_type',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

